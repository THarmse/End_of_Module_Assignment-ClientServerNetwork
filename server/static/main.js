// Initialize an empty object to hold key-value pairs
let data = {};

// Once the DOM is fully loaded, add event listeners
document.addEventListener("DOMContentLoaded", function () {
  // Attach event listener to the format dropdown to update the serialized output when changed
  document.getElementById("format").addEventListener("change", function () {
    showSerializedOutput();
  });
});

/**
 * Function to add key-value pairs to the data object and display it.
 */
function addData() {
  // Retrieve the entered key and value from the input fields
  const key = document.getElementById("key").value;
  const value = document.getElementById("value").value;

  // Add the key-value pair to the data object
  data[key] = value;

  // Display the current key-value pairs as a formatted JSON string
  document.getElementById("currentData").textContent = JSON.stringify(data, null, 4);

  // Update the display of the serialized output
  showSerializedOutput();
}

/**
 * Function to display the data object in the chosen serialization format.
 */
function showSerializedOutput() {
  // Retrieve the selected serialization format
  const format = document.getElementById('format').value;

  let output = ""; // Initialize an empty string to hold the serialized output

  // Serialize the data based on the chosen format
  if (format === "JSON") {
    output = JSON.stringify(data, null, 4); // Pretty-print JSON with 4-space indentation
  } else if (format === "XML") {
    // Manually create an XML-like string for demonstration purposes
    output = "<root>\n";
    for (let key in data) {
      output += "  <item>\n";
      output += `    <key>${key}</key>\n`;
      output += `    <value>${data[key]}</value>\n`;
      output += "  </item>\n";
    }
    output += "</root>";
  } else if (format === "Binary") {
    // Simulate Binary data by encoding the JSON string in base64
    const jsonString = JSON.stringify(data);
    const base64String = btoa(jsonString);
    output = `Simulated base64-encoded pickled data: ${base64String}`;
  }

  // Display the serialized output
  document.getElementById('serializedOutput').textContent = output;
}

/**
 * Function to submit the data to the server.
 */
function submitData() {
  // Retrieve form data
  const serializeFormat = document.getElementById("format").value;
  const encrypt = document.getElementById("encrypt").checked;
  const asTextFile = document.getElementById("asTextFile").checked;

  // Make an HTTP POST request to the server
  fetch("/send_data", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      data: data,
      format: serializeFormat,
      encrypt: encrypt,
      asTextFile: asTextFile,
    }),
  })
  .then((response) => response.json()) // Parse the JSON response from the server
  .then((data) => {
    console.log("Success:", data); // Log the server's response for debugging
  })
  .catch((error) => {
    console.error("Error:", error); // Log any errors for debugging
  });
}
