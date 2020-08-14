const currentTheme = localStorage.getItem("theme");

if (currentTheme == null) { // On first load
    lightMode();
}
else if (currentTheme == "light") {
    lightMode();
}
else {
    darkMode();
}

function darkMode() {
    localStorage.setItem("theme","dark");
    document.body.setAttribute('data-theme', 'dark');
}

function lightMode() {
    localStorage.setItem("theme","light");
    document.body.removeAttribute('data-theme');
}

function toggle() { // Won't be null by now
    const theme = localStorage.getItem("theme");
    if (theme == "dark") {
        lightMode();
    }
    else {
        darkMode();
    }
}