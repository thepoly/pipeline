// Varaibles Declarations (DOM Elements request)
var body = document.body;
var navscroller = document.getElementsByClassName('nav-scroller')[0];
var footer = document.getElementsByClassName('footer')[0];
var links = document.getElementsByTagName("a");
var headers = document.getElementsByTagName("h3");
var captions = document.getElementsByClassName("caption");
var button = document.getElementById('btnSwitch');

// Local Storage Request For Previously Stored Light or Dark Theme information
var currentTheme = localStorage.getItem("theme");

//Preset all links and headers to be dark
for(i = 0; i < links.length; i++){

  //Ignore the top subsribe button
  if(links[i].id == "subscribe"){
    links[i].classList.add("text-light");
    continue;
  } 
  links[i].classList.add('text-dark');
}
for(i = 0; i < headers.length; i++){
  headers[i].classList.add('text-dark');
}


//Immediately toggle to dark if that is the desired preference
if (currentTheme == "dark") {
  toggle();
  //Remain light if the preference is light
}


//Function to toggle the specific classes from a dark background
function toggle(){
    //Toggle main body text
    body.classList.toggle("text-light");
    body.classList.toggle("bg-dark");
    //Toggle under header
    navscroller.classList.toggle("bg-dark");
    navscroller.classList.toggle("bg-gradient");
    //Toggle bottom footer
    footer.classList.toggle("bg-dark");
    //Toggle every link (defined seperately than text)
    for(i = 0; i < links.length; i++){
      if(links[i].id == "subscribe"){
        continue;
      } 
      links[i].classList.toggle('text-dark');
      links[i].classList.toggle('text-light');
    }
    //Toggle every captions (defined seperately than text)
    for(i = 0; i < captions.length; i++){
      captions[i].classList.toggle('text-dark');
      captions[i].classList.toggle('text-light');
    }
    //Toggle every captions (defined seperately than text)
    for(i = 0; i < headers.length; i++){
      headers[i].classList.toggle('text-dark');
      headers[i].classList.toggle('text-light');
   }
}

//Actual button event trigger
document.getElementById('btnSwitch').addEventListener('mouseup',()=>{
  //Reset all variables in case of page change
  body = document.body;
  navscroller = document.getElementsByClassName('nav-scroller')[0];
  links = document.getElementsByTagName("a");
  var headers = document.getElementsByTagName("h3");
  captions = document.getElementsByClassName("caption");

  //Toggle light from dark
  toggle();

  //Toggle local variable to keep track of positive and negative values.
  var currentTheme = localStorage.getItem("theme");
  var themecolor = currentTheme == "dark" ? "light" : "dark";
  localStorage.setItem("theme", themecolor);
});


