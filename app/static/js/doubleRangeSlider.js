export function createDoubleRangeSlider(containerId, startInputId, endInputId, min, max, onChangeCallback = null) {
  const container = document.getElementById(containerId);
  container.innerHTML = `
      <div class="range-slider">
          <input type="range" id="${startInputId}" name="${startInputId}" min="${min}" max="${max}">
          <input type="range" id="${endInputId}" name="${endInputId}" min="${min}" max="${max}">
      </div>
  `;

  const startInput = document.getElementById(startInputId);
  const endInput = document.getElementById(endInputId);
  // const startLabel = document.getElementById(`${startInputId}-label`);
  // const endLabel = document.getElementById(`${endInputId}-label`);

  // const updateLabels = () => {
  //   startLabel.textContent = startInput.value;
  //   endLabel.textContent = endInput.value;
  // };

  startInput.addEventListener('input', () => {
    if (parseInt(startInput.value) > parseInt(endInput.value)) {
      startInput.value = endInput.value;
    }
    // updateLabels();
    // Call the callback function if it is provided (optional, e.g. updating a graph)
    if (onChangeCallback) onChangeCallback();
  });

  endInput.addEventListener('input', () => {
    if (parseInt(endInput.value) < parseInt(startInput.value)) {
      endInput.value = startInput.value;
    }
    // updateLabels();
    // Call the callback function if it is provided (optional, e.g. updating a graph)
    if (onChangeCallback) onChangeCallback();
  });

  // Initial update of the labels
  // updateLabels();
}
