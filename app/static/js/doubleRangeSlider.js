document.addEventListener('DOMContentLoaded', () => {
  const yearRangeSliderContainer = document.getElementById('year-range-slider');
  const educationLevelSliderContainer = document.getElementById('education-level-slider');

  yearRangeSliderContainer.innerHTML = `
    <label for="year-range">Select Year Range:</label>
    <div class="range-slider">
      <input type="range" id="start-year" name="start-year" min="2000" max="2020">
      <input type="range" id="end-year" name="end-year" min="2000" max="2020">
    </div>
  `;

  educationLevelSliderContainer.innerHTML = `
    <label for="education-level-range">Select Education Level:</label>
    <div class="range-slider">
      <input type="range" id="start-education-level" name="start-education-level" min="1" max="5">
      <input type="range" id="end-education-level" name="end-education-level" min="1" max="5">
    </div>
  `;

  // Logic to synchronize the two sliders if needed
  const synchronizeSliders = (startSlider, endSlider) => {
    startSlider.addEventListener('input', () => {
      if (parseInt(startSlider.value) > parseInt(endSlider.value)) {
        startSlider.value = endSlider.value;
      }
    });
    endSlider.addEventListener('input', () => {
      if (parseInt(endSlider.value) < parseInt(startSlider.value)) {
        endSlider.value = startSlider.value;
      }
    });
  };

  synchronizeSliders(document.getElementById('start-year'), document.getElementById('end-year'));
  synchronizeSliders(document.getElementById('start-education-level'), document.getElementById('end-education-level'));
});
