function updateImage() {
    var select = document.getElementById("imageSelect");
    var image = document.getElementById("displayedImage");
    image.src = select.value;
}