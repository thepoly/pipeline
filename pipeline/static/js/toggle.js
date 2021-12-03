// Varaibles Declarations (DOM Elements request)
var body = document.body;
var navscroller = document.getElementsByClassName('nav-scroller')[0];
var footer = document.getElementsByClassName('footer')[0];
var links = document.getElementsByTagName("a");
var headers = document.getElementsByTagName("h3");
var currentTheme = localStorage.getItem("theme");

for(i = 0; i < links.length; i++){
  links[i].classList.add('text-dark');
}
for(i = 0; i < headers.length; i++){
  headers[i].classList.add('text-dark');
}
var button = document.getElementById('btnSwitch');

if (currentTheme == "dark") {
  //Immediately toggle to dark if that is the desired preference
  toggle();
  //Remain light if the preference is light
}
//Function to toggle the specific classes from a dark background
function toggle(){
    body.classList.toggle("text-light");
    body.classList.toggle("bg-dark");
    navscroller.classList.toggle("bg-dark");
    footer.classList.toggle("bg-dark");
    for(i = 0; i < links.length; i++){
       links[i].classList.toggle('text-dark');
       links[i].classList.toggle('text-light');

    }
    for(i = 0; i < headers.length; i++){
      headers[i].classList.toggle('text-dark');
      headers[i].classList.toggle('text-light');
   }
}
document.getElementById('btnSwitch').addEventListener('mouseup',()=>{
  body = document.body;
  navscroller = document.getElementsByClassName('nav-scroller')[0];
  links = document.getElementsByTagName("a");
  var headers = document.getElementsByTagName("h3");
  button = document.getElementById('btnSwitch');
  toggle();
  var currentTheme = localStorage.getItem("theme");
  var themecolor = currentTheme == "dark" ? "light" : "dark";
  localStorage.setItem("theme", themecolor);
});


