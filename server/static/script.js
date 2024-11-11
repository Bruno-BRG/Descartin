function updateImage() {
    var select = document.getElementById("imageSelect");
    var image = document.getElementById("displayedImage");
    image.src = select.value;
}

// script.js
function filterImages() {
  const residueFilter = document.getElementById('residue-type').value.toLowerCase();
  const startDate = parseInt(document.getElementById('start-date').value);
  const endDate = parseInt(document.getElementById('end-date').value);
  const images = document.querySelectorAll('.residue-image');

  images.forEach(image => {
    const imageResidue = image.alt.toLowerCase();
    const imageYear = parseInt(image.getAttribute('data-year'));

    if ((residueFilter === 'all' || imageResidue === residueFilter) &&
        (!startDate || imageYear >= startDate) &&
        (!endDate || imageYear <= endDate)) {
      image.style.display = 'block';
    } else {
      image.style.display = 'none';
    }
  });
}