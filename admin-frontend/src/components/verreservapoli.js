import React, { useEffect, useState } from 'react';
import { API_URL } from '../config';
import { esFechaPasada, exportarPDF, fechaLocal } from '../utils/reportes';


const VerReservaPoli = () => {
  const [reservasPoli, setReservasPoli] = useState([]);
  const [horarios, setHorarios] = useState([]);
  const [polideportivos, setPolideportivos] = useState([]);
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedDate, setSelectedDate] = useState(fechaLocal());
  const [llegoReserva, setLlegoReserva] = useState({});
  const handleDateChange = (event) => {
    setSelectedDate(event.target.value);
  };
  
  
  const filteredReservas = reservasPoli.filter((r) => r.fecha === selectedDate);

  const handleLlegoChange = (id) => {
    setLlegoReserva((prevLlegoReserva) => ({
      ...prevLlegoReserva,
      [id]: !prevLlegoReserva[id],
    }));
  };
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const reservasResponse = await fetch(`${API_URL}/reservapolideportivos/`);
        const reservasPoliData = await reservasResponse.json();
        setReservasPoli(reservasPoliData);
  
        const horariosResponse = await fetch(`${API_URL}/horarios/`);
        const horariosData = await horariosResponse.json();
        setHorarios(horariosData);
  
        const polideportivosResponse = await fetch(`${API_URL}/polideportivos/`);
        const polideportivosData = await polideportivosResponse.json();
        setPolideportivos(polideportivosData);
  
        const usuariosResponse = await fetch(`${API_URL}/usuarios/`);
        const usuariosData = await usuariosResponse.json();
        setUsuarios(usuariosData);
  
        setLoading(false);
  
      } catch (error) {
        console.error('Error fetching reservations:', error);
      }
    };
  
    fetchData();
  }, []);

  const isReservaPasada = esFechaPasada;
  

  const handleGeneratePDF = () => {
    exportarPDF({
      titulo: `Reservas de polideportivos - ${selectedDate}`,
      columnas: ['Fecha', 'Hora inicio', 'Hora fin', 'Polideportivo', 'Cod. estudiante', 'Llegó'],
      filas: filteredReservas.map((r) => {
        const horario = horarios.find((h) => h.id === r.Horario);
        const espacio = polideportivos.find((e) => e.id === r.polideportivo);
        const usuario = usuarios.find((u) => u.id === r.Usuario);
        return [r.fecha, horario?.hora_inicio ?? 'N/A', horario?.hora_fin ?? 'N/A', espacio?.nombre ?? 'N/A', usuario?.codigo ?? 'N/A', llegoReserva[r.id] ? 'Sí' : 'No'];
      }),
      archivo: `reservas_polideportivos_${selectedDate}.pdf`,
    });
  };

  if (loading) {
    return <p>Cargando datos...</p>;
  }

  return (
    <div>
      <header className="bg-dark text-white">
        <div className="container py-2">
          <div className="d-flex flex-wrap align-items-center justify-content-center">
            <a href="/" className="d-flex align-items-center text-white text-decoration-none">
              <img src="/logo.png" alt="TECSITE Logo" width="120" height="120" className="logo" />
            </a>
          </div>
        </div>
      </header>

      <div className="container mt-4">
        <h2 className="mb-4">Reservas de Polideportivos</h2>
        
        <div className="mb-3">
          <label htmlFor="dateFilter" className="form-label">Filtrar por fecha:</label>
          <input
            type="date"
            id="dateFilter"
            className="form-control"
            value={selectedDate}
            onChange={handleDateChange}
          />
        </div>

        <table className="table table-striped table-bordered">
          <thead className="thead-dark">
            <tr>
              <th scope="col">Fecha de reserva</th>
              <th scope="col">Hora Inicio</th>
              <th scope="col">Hora Fin</th>
              <th scope="col">Nombre del polideportivo</th>
              <th scope="col">Cod. Estudiante</th>
              <th scope="col">Asistencia</th>
            </tr>
          </thead>
          <tbody>
          {filteredReservas.map((reservaPoli) => {
  const horarioEncontrado = horarios.find((horario) => horario.id === reservaPoli.Horario);
  const polideportivoEncontrado = polideportivos.find((polideportivo) => polideportivo.id === reservaPoli.polideportivo);
  const usuarioEncontrado = usuarios.find((usuario) => usuario.id === reservaPoli.Usuario);
  const reservaPasada = isReservaPasada(reservaPoli.fecha);

  return (
    <tr
      key={reservaPoli.id}
      className={`${reservaPasada ? 'reserva-pasada' : ''} ${llegoReserva[reservaPoli.id] ? 'reserva-llego' : ''}`}
      disabled={reservaPasada}
    >
      <td>{reservaPoli.fecha}</td>
      <td>{horarioEncontrado ? horarioEncontrado.hora_inicio : 'N/A'}</td>
      <td>{horarioEncontrado ? horarioEncontrado.hora_fin : 'N/A'}</td>
      <td>{polideportivoEncontrado ? polideportivoEncontrado.nombre : 'N/A'}</td>
      <td>{usuarioEncontrado ? usuarioEncontrado.codigo : 'N/A'}</td>
      <td>
        <input
          type="checkbox"
          checked={llegoReserva[reservaPoli.id] || false}
          onChange={() => handleLlegoChange(reservaPoli.id)}
          disabled={reservaPasada}
        />
        Llegó
      </td>
    </tr>
  );
})}
          </tbody>
        </table>
        {filteredReservas.length === 0 && (
          <p className="text-muted">No hay reservas para esta fecha.</p>
        )}
        <div className="button-group d-flex gap-2">
          <a href="/" className="btn btn-lg btn-primary mt-3">Regresar</a>
          <button type="button" className="btn btn-lg btn-outline-dark mt-3" onClick={handleGeneratePDF}
            disabled={filteredReservas.length === 0}>Descargar PDF</button>
        </div>
      </div>
    </div>
  );
};

export default VerReservaPoli;
