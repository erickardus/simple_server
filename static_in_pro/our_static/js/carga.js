// Script de jQuery que carga a tabla un archivo .txt dado (fileName)

// Una vez que cargue el documento...
$(document).ready(function() {
	 setTimeout(function(){
	 	$("#lesen").load("{% static 'salidas/interactive' %}"); 
    }, 5 * 1000);
});
	// load();
	// var refreshInterval = setInterval(load, 5 * 1000);	
// });
//funcion que carga el archivo
// function load()	{
    // $("#lesen").load('../../../chef-provisioning/interactive.txt');
// }
