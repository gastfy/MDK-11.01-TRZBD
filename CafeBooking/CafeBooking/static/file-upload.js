var file = document.querySelector("[name='file']");

file.addEventListener('change', function() {
    var text = document.querySelector("[name='file-name']");
	var file_uploaded = file.files[0];  
   	var filename = file_uploaded.name;
	text.textContent = filename
});

var form = document.forms[0]
form.addEventListener('submit', function(e){
	console.log(file.files.length);

	if (file.files.length <= 0) {
		e.preventDefault()
		return false
	}

	if (window.confirm("Несохраненные данные удалятся. Вы уверены?")){
		return true
	}
	e.preventDefault()
	return false
});