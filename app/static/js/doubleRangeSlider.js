export function createDoubleRangeSlider(containerId, startInputId, endInputId, onChange) {
  const container = document.getElementById(containerId);
  container.innerHTML = `
      <div class="range-slider">
          <input type="range" id="${startInputId}" name="${startInputId}" min="2000" max="2020">
          <input type="range" id="${endInputId}" name="${endInputId}" min="2000" max="2020">
      </div>
  `;

  const startInput = document.getElementById(startInputId);
  const endInput = document.getElementById(endInputId);

  startInput.addEventListener('input', () => {
    if (parseInt(startInput.value) > parseInt(endInput.value)) {
      startInput.value = endInput.value;
    }
    onChange();
  });

  endInput.addEventListener('input', () => {
    if (parseInt(endInput.value) < parseInt(startInput.value)) {
      endInput.value = startInput.value;
    }
    onChange();
  });
}
