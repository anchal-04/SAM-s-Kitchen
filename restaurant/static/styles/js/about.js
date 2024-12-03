document.addEventListener("DOMContentLoaded", () => {
  const carousel = document.getElementById("carousel");
  const leftArrow = document.getElementById("left-arrow");
  const rightArrow = document.getElementById("right-arrow");

  // Check if elements are loaded properly
  if (!carousel || !leftArrow || !rightArrow) {
    console.error("Carousel or arrow elements not found!");
    return;
  }

  // Scroll Left
  leftArrow.addEventListener("click", () => {
    carousel.scrollBy({
      left: -300, // Adjust scroll amount as needed
      behavior: "smooth",
    });
  });

  // Scroll Right
  rightArrow.addEventListener("click", () => {
    carousel.scrollBy({
      left: 300, // Adjust scroll amount as needed
      behavior: "smooth",
    });
  });
});
