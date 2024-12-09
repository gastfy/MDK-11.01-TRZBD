function setTheme(themeName) {
    document.documentElement.className = themeName;
    localStorage.setItem('theme', themeName);
}

const theme = localStorage.getItem('theme');
if (theme) {
	if (theme === 'theme-dark') {
		setTheme('theme-dark');
	} 

	if (theme === 'theme-light') {
		setTheme('theme-light');
	}
}
else {
	localStorage.setItem('theme', 'theme-dark')
}

var button = document.querySelector("[name='scheme-changer']")
button.addEventListener('click', function() {
	const theme = localStorage.getItem('theme');
	if (theme) {
		if (theme === 'theme-dark') {
			setTheme('theme-light');
		} 
	
		if (theme === 'theme-light') {
			setTheme('theme-dark');
		}
	}
});

