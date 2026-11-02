import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

// Fecha local en formato YYYY-MM-DD (toISOString usa UTC y en Lima cambia de día a las 7 p. m.)
export const fechaLocal = (date = new Date()) => {
  const pad = (n) => String(n).padStart(2, '0');
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
};

// Las fechas de la API vienen como 'YYYY-MM-DD'; se comparan como texto para no depender de la zona horaria.
export const esFechaPasada = (fecha) => fecha < fechaLocal();

export const exportarPDF = ({ titulo, columnas, filas, archivo }) => {
  const doc = new jsPDF();
  doc.setFontSize(14);
  doc.text(titulo, 14, 15);
  autoTable(doc, { head: [columnas], body: filas, startY: 22, headStyles: { fillColor: [33, 37, 41] } });
  doc.save(archivo);
};
