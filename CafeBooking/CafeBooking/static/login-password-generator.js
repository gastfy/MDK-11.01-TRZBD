var form = document.forms[0];

var generate_login = form.querySelector('[name="generate-login"]');
var generate_pass = form.querySelector('[name="generate-password"]');
var show_password = form.querySelector('[name="show-password"]');
var login_input = form.querySelector('[name="login"]');
var password_input = form.querySelector('[name="password"]');

function generatePass() {
    let pass = '';
    let str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' +
        'abcdefghijklmnopqrstuvwxyz0123456789@#$';

    for (let i = 1; i <= 12; i++) {
        let char = Math.floor(Math.random()
            * str.length + 1);

        pass += str.charAt(char)
    }

    return pass;
}

function generateLogin() {
    let pass = '';
    let str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' +
        'abcdefghijklmnopqrstuvwxyz0123456789';

    for (let i = 1; i <= 8; i++) {
        let char = Math.floor(Math.random()
            * str.length + 1);

        pass += str.charAt(char)
    }

    return pass;
}


generate_login.addEventListener('click', function(e){
	login_input.value = generateLogin();
});

generate_pass.addEventListener('click', function(e){
	password_input.value = generatePass();
});

show_password.addEventListener('click', function(e){
	if (password_input.type === "password"){
		password_input.type = "text";
		show_password.innerHTML = "<span class='icon is-small'><i class='fa-solid fa-eye-slash'></i></span>"
	}
	else {
		password_input.type = "password";
		show_password.innerHTML = "<span class='icon is-small'><i class='fa-solid fa-eye'></i></span>"
	}
})