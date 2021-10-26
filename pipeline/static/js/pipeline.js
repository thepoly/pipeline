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

import { Controller } from "stimulus"

export default class extends Controller {
  greet() {
    console.log(`Hello, ${this.name}!`)
  }

  get name() {
    return this.targets.find("name").value
  }
}