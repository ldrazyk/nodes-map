console.log("Script 'script.js' loaded.")

const selectFile = function(file) {
    document.getElementById('nodes_file').value = file
    console.log("File: '" + file + "' selected.")
}