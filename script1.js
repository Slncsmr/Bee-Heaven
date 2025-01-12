// Wait for the document to fully load before attaching event listeners
document.addEventListener('DOMContentLoaded', function () {
    // Attach the event listener to the form
    document.getElementById('inspectionForm').addEventListener('submit', function (event) {
        // Prevent the default form submission (to avoid page reload)
        event.preventDefault();

        // Get the form values
        const date = document.getElementById('date').value;
        const weather = document.getElementById('weather').value;
        const notes = document.getElementById('Notes').value;

        // Collect all checkbox values
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        const selectedCheckboxes = [];

        checkboxes.forEach(function (checkbox) {
            if (checkbox.checked) {
                selectedCheckboxes.push(checkbox.name);
            }
        });

        // Prepare the data to be saved
        const formData = {
            date: date,
            weather: weather,
            selectedCheckboxes: selectedCheckboxes,
            notes: notes
        };

        // Convert the data to a JSON string
        const fileContent = JSON.stringify(formData, null, 2);

        // Create a Blob from the JSON data (this simulates a file)
        const blob = new Blob([fileContent], { type: 'application/json' });

        // Create a temporary download link
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob); // Create a URL for the Blob
        link.download = 'inspectionData.json'; // Specify the default filename for download

        // Trigger a click on the link to download the file
        link.click();
    });
});
