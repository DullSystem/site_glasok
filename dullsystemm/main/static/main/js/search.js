function first() {

document.getElementById("second_hide").setAttribute("style",  "opacity:1; transition: 3s; height: 100%; );

document.getElementById("first").setAttribute("style", "display: block");

document.getElementById("first_yelloy").setAttribute("style", "display: none");

}

function first_yelloy() {

document.getElementById("second_hide").setAttribute("style", "display: block");

document.getElementById("first_yelloy").setAttribute("style", "display: none");

document.getElementById("first").setAttribute("style", "display: none");

}