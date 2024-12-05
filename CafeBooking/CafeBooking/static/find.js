var finder = document.querySelector("[name='finder']");

finder.addEventListener('keyup', function(e){
	finder_value = finder.value;
	table = document.getElementById("my_table");
	tr = table.getElementsByTagName("tr");

	for (i = 0; i < tr.length; i++) {
		td = tr[i].getElementsByTagName("td")[1];
		if (finder_value != ""){
			if (td) {
				txtValue = td.textContent || td.innerText;
				if (txtValue.indexOf(finder_value) > -1) {
					tr[i].classList.add("is-selected");
				} else {
				  tr[i].classList.remove("is-selected");
				}
			  }
		}
		else {
			if (td) {
				tr[i].classList.remove("is-selected")
			}
		}
	  }

});