import { Controller } from "stimulus"

export default class extends Controller {
    static targets = ["scroller"];
    evaluating = false;

    connect() {
        this.evaluating = true;
        this.evaluateShow();
    }

    evaluateShow() {
        if (window.scrollY >= 200) {
            this.scrollerTarget.classList.add("home-link--show");
        } else {
            this.scrollerTarget.classList.remove("home-link--show");
        }
        this.evaluating = false;
    }

    onScroll(event) {
        if (this.evaluating) {
            return;
        }
        this.evaluating = true;
        if (window.requestAnimationFrame) {
            window.requestAnimationFrame(() => this.evaluateShow());
        } else {
            this.evaluateShow();
        }
    }
}
