// Function to get the current date and generate the next 7 days
function getNext7Days() {
    const today = new Date();
    const days = [];

    for (let i = 0; i < 7; i++) {
        const date = new Date(today);
        date.setDate(today.getDate() + i);
        days.push(date);
    }

    return days;
}

// Function to render the forecast data
async function renderForecast() {
    const forecastContainer = document.getElementById('forecast');
    const days = getNext7Days();
    forecastContainer.innerHTML = ''; // Clear previous content

    try {
        // Fetch the weather data for the user's location (Replace with your coordinates)
        const latitude = 38.8977; // Example: Latitude for Washington DC
        const longitude = -77.0365; // Example: Longitude for Washington DC

        // Step 1: Get the grid point for the forecast
        const pointsResponse = await fetch(`https://api.weather.gov/points/${latitude},${longitude}`);
        if (!pointsResponse.ok) throw new Error(`Failed to fetch grid data: ${pointsResponse.status}`);
        const pointsData = await pointsResponse.json();
        const forecastUrl = pointsData.properties.forecast;

        // Step 2: Fetch the forecast data
        const forecastResponse = await fetch(forecastUrl);
        if (!forecastResponse.ok) throw new Error(`Failed to fetch forecast data: ${forecastResponse.status}`);
        const forecastData = await forecastResponse.json();

        // Step 3: Generate forecast cards for each day
        forecastData.properties.periods.slice(0, 7).forEach((day, index) => {
            const card = document.createElement('div');
            card.classList.add('forecast-card');
            card.innerHTML = `
                <div class="icon">
                    <img src="${day.icon}" alt="${day.shortForecast}" />
                </div>
                <div class="day">${days[index].toLocaleString('en-us', { weekday: 'short' })}</div>
                <div class="temperature">${day.temperature}&deg;${day.temperatureUnit}</div>
                <div class="condition">${day.shortForecast}</div>
                <div class="date">${days[index].toLocaleDateString()}</div>
            `;
            card.addEventListener('click', () => showMoreInfo(day, days[index]));
            forecastContainer.appendChild(card);
        });
    } catch (error) {
        console.error('Error fetching weather data:', error);
        alert('Error fetching weather data');
    }
}

// Function to show more information about a day when clicked
function showMoreInfo(day, date) {
    const extraInfoContainer = document.getElementById('extra-info');
    const extraDetails = document.getElementById('extra-details');
    extraDetails.innerHTML = `
        <strong>Weather:</strong> ${day.shortForecast}<br />
        <strong>Temperature:</strong> ${day.temperature}&deg;${day.temperatureUnit}<br />
        <strong>Wind:</strong> ${day.windSpeed} ${day.windDirection}<br />
        <strong>Time of Forecast:</strong> ${date.toLocaleString('en-us', { weekday: 'long', month: 'long', day: 'numeric' })}
    `;
    extraInfoContainer.style.display = 'block';
}

// Close the extra info panel
document.getElementById('close-info').addEventListener('click', () => {
    document.getElementById('extra-info').style.display = 'none';
});

// Initialize the forecast
renderForecast();
