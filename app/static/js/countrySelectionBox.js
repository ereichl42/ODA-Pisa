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

export function populateFinanceMetrics(metrics) {
  const metricSelectionContainer = document.getElementById('finance-metric-selection-box');

  const selectHTML = document.createElement('select');
  selectHTML.setAttribute('id', 'finance-metrics');
  selectHTML.setAttribute('name', 'finance-metrics');

  metrics.forEach(metric => {
    const option = document.createElement('option');
    option.setAttribute('value', metric); // Setting the value attribute to the metric name
    option.textContent = metric.replace(/_/g, ' ').toUpperCase(); // Setting text content to metric name in uppercase
    selectHTML.appendChild(option);
  });

  metricSelectionContainer.innerHTML = ''; // Clear previous content
  metricSelectionContainer.appendChild(selectHTML);
}
