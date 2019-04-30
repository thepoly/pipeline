import { Controller } from "stimulus"

export default class extends Controller {
    static targets = ["photo", "largePhoto", "largePhotoImg", "largePhotoCaption", "largePhotoPhotographer"];

    connect() { }

    // load in the photo that we hover over to speed things up
    hoverPhoto(event) {
        event.preventDefault();
        this.preparePhoto(event.target);
    }

    showPhoto(event) {
        event.preventDefault();
        this.preparePhoto(event.target);

        this.largePhotoTarget.classList.toggle("large-photo--show");

        // prevent body scrolling behind photo
        const body = document.getElementsByTagName('body')[0];
        body.classList.toggle('modal-open');
    }

    preparePhoto(target) {
        const index = this.photoTargets.indexOf(target);
        this.data.set("index", index);

        const largeSrc = event.target.getAttribute("data-large-src");
        const caption = event.target.getAttribute("data-caption");
        const photographer = event.target.getAttribute("data-photographer");
        this.largePhotoImgTarget.src = event.target.getAttribute("data-large-src");
        this.largePhotoCaptionTarget.innerHTML = caption;
        this.largePhotoPhotographerTarget.innerHTML = photographer;
    }

    dismissPhoto(event) {
        this.largePhotoTarget.classList.toggle("large-photo--show");
        this.largePhotoImgTarget.removeAttribute("src");

        // re-enable body scroll
        const body = document.getElementsByTagName('body')[0];
        body.classList.toggle('modal-open');
    }
}
