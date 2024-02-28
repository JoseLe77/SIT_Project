// Obtenemos los elementos del DOM que vamos a utilizar
const toolNumberSelect = document.getElementById("tool_number");
const toolNameInput = document.getElementById("tool_name");
const toolUrlInput = document.getElementById("tool_url");

// Escuchamos el evento "change" del select
toolNumberSelect.addEventListener("change", function() {
  // Obtenemos el valor seleccionado en el select
  const selectedNumber = toolNumberSelect.value;
  // Actualizamos el valor de los inputs de nombre y URL de acuerdo al número seleccionado
  toolNameInput.value = "{{ all_tools_results." + (selectedNumber) + ".1 }}";
  toolUrlInput.value = "{{ all_tools_results." + (selectedNumber) + ".2 }}";
});
