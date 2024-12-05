var filter = document.querySelector("[name='find_by_id']");

filter.addEventListener('keyup', function(e){
	filter_value = filter.value;
	table = document.getElementById("my_table");
	tr = table.getElementsByTagName("tr");
  
	// Loop through all table rows, and hide those who don't match the search query
	for (i = 0; i < tr.length; i++) {
	  td = tr[i].getElementsByTagName("td")[0];
	  if (td) {
		txtValue = td.textContent || td.innerText;
		if (txtValue.indexOf(filter_value) > -1) {
		  tr[i].style.display = "";
		} else {
		  tr[i].style.display = "none";
		}
	  }
	}
});