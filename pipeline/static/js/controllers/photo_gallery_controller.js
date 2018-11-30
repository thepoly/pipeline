import { Controller } from "stimulus"

export default class extends Controller {
    static targets = ["photo", "largePhoto", "largePhotoImg", "largePhotoCaption", "largePhotoPhotographer"];

    connect() {
        console.log("hey");
    }

    showPhoto(event) {
        event.preventDefault();
        console.log("showPhoto");
        let index = this.photoTargets.indexOf(event.target);
        this.data.set("index", index);
        console.log(index);

        const largeSrc = event.target.getAttribute("data-large-src");
        const caption = event.target.getAttribute("data-caption");
        const photographer = event.target.getAttribute("data-photographer");
        this.largePhotoImgTarget.src = event.target.getAttribute("data-large-src");
        this.largePhotoCaptionTarget.innerText = caption;
        this.largePhotoPhotographerTarget.innerText = photographer;

        this.largePhotoTarget.classList.toggle("large-photo--show");
    }

    dismissPhoto(event) {
        console.log("hi");
        this.largePhotoTarget.classList.toggle("large-photo--show");
    }
}
