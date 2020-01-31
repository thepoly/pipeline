// Turbolinks
import Turbolinks from 'turbolinks';
Turbolinks.start();

// Stimulus
import { Application } from "stimulus"
import { definitionsFromContext } from "stimulus/webpack-helpers"
const application = Application.start();
const context = require.context("./controllers", true, /\.(js|ts)$/);
application.load(definitionsFromContext(context));

// Google Analytics
document.addEventListener("turbolinks:load", (event) => {
    if (typeof ga === "function") {
        ga('set', 'location', event.data.url);
        ga('send', 'pageview');
    }
});

//lightbox2
import * as lightbox from "lightbox2";
lightbox.option({
        'imageFadeDuration': 0,
        'fadeDuration': 0,
        'showImageNumberLabel': 0,
        'resizeDuration': 10, //this cannot be less or else it will send the user to the top of the page
        'wrapAround': true,
        'disableScrolling': true
});