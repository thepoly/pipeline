// Turbolinks
import Turbolinks from 'turbolinks';
Turbolinks.start();

// Stimulus
import { Application } from "stimulus"
import { definitionsFromContext } from "stimulus/webpack-helpers"
const application = Application.start();
const context = require.context("./controllers", true, /\.(js|ts)$/)
application.load(definitionsFromContext(context))
