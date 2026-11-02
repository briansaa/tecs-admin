import React, { useEffect, useState } from 'react';
import { API_URL } from '../config';

const Verlab = () => {
  const [data, setData] = useState([]);
  const [pabellones, setPabellones] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`${API_URL}/laboratorios/`);
        const jsonData = await response.json();
        setData(jsonData);
        const pabRes = await fetch(`${API_URL}/pabellones/`);
        const pabData = await pabRes.json();
        setPabellones(Object.fromEntries(pabData.map((p) => [p.id, p.nombre])));
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);

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
        <h2 className="mb-4">Lista de Laboratorios</h2>
        <table className="table table-striped table-bordered">
          <thead className="thead-dark">
            <tr>
              <th scope="col">Nombre del Laboratorio</th>
              <th scope="col">Pabellón</th>
            </tr>
          </thead>
          <tbody>
            {data.map(item => (
              <tr key={item.nombre}>
                <td>{item.nombre}</td>
                <td>{pabellones[item.pabellon] ?? item.pabellon}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="button-group">
          <a href="/" className="btn btn-lg btn-primary mt-3">Regresar</a>
        </div>
      </div>
    </div>
  );
};

export default Verlab;
