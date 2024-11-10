function updateImage() {
    var select = document.getElementById("imageSelect");
    var image = document.getElementById("displayedImage");
    image.src = select.value;
}

// script.js
function filterImages() {
  const filter = document.getElementById('residue-type').value.toLowerCase();
  const images = document.querySelectorAll('.residue-image');

  images.forEach(image => {
    if (filter === 'all' || image.alt.toLowerCase() === filter) {
      image.style.display = 'block';
    } else {
      image.style.display = 'none';
    }
  });
}