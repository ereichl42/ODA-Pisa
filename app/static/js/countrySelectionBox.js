document.addEventListener('DOMContentLoaded', () => {
    const countrySelectionContainer = document.getElementById('country-selection');
    countrySelectionContainer.innerHTML = `
      <label for="countries">Select Countries:</label>
      <select id="countries" name="countries" multiple>
        <option value="USA">USA</option>
        <option value="Canada">Canada</option>
        <option value="UK">UK</option>
        <option value="Germany">Germany</option>
        <!-- Add more options as needed -->
      </select>
    `;
});
