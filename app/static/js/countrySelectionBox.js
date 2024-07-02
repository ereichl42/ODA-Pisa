export function populateCountries(countries) {
  const countrySelectionContainer = document.getElementById('country-selection-box');
  const countriesList = countries.countries; // Accessing the countries object from the provided JSON

  const selectHTML = document.createElement('select');
  selectHTML.setAttribute('id', 'countries');
  selectHTML.setAttribute('name', 'countries');
  selectHTML.setAttribute('multiple', true);

  for (const [name, code] of Object.entries(countriesList)) {
    const option = document.createElement('option');
    option.setAttribute('value', code); // Setting the value attribute to the country code
    option.textContent = name; // Setting the text content to the country name
    selectHTML.appendChild(option);
  }

  countrySelectionContainer.innerHTML = ''; // Clear previous content
  countrySelectionContainer.appendChild(selectHTML);
}
