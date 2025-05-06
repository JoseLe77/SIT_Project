function filtrarTabla() {
  const input = document.getElementById('miBusqueda');
  const filtro = input.value.toUpperCase();
  const tabla = document.getElementById("tabla");
  const tr = tabla.getElementsByTagName('tr');

  for (let i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0]; // Ajusta el índice si quieres buscar en otra columna
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filtro) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}