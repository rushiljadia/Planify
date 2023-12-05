console.log("Dashboard js is working");

function disableFormFields() {
  var checkbox = document.getElementById("has_lab");
  var labDay = document.getElementById("lab_day");
  var labStartTime = document.getElementById("lab_start_time");
  var labEndTime = document.getElementById("lab_end_time");

  if (checkbox.checked) {
    labDay.disabled = false;
    labStartTime.disabled = false;
    labEndTime.disabled = false;
  } else {
    labDay.disabled = true;
    labStartTime.disabled = true;
    labEndTime.disabled = true;
  }
}

// Dashboard js
console.log("Dashboard js is working");

// Function to handle button click
function handleAddClassClick(button) {
  const courseInfo = {
    code: button.getAttribute("data-course-code"),
    name: button.getAttribute("data-course-name"),
    place: button.getAttribute("data-course-place"),
    days: button.getAttribute("data-course-days"),
    startTime: button.getAttribute("data-course-start-time"),
    endTime: button.getAttribute("data-course-end-time"),
    hasLab: button.getAttribute("data-course-has-lab"),
    labDay: button.getAttribute("data-course-lab-day"),
    labStartTime: button.getAttribute("data-course-lab-start-time"),
    labEndTime: button.getAttribute("data-course-lab-end-time"),
  };

  // Use fetch to send a POST request to the '/add-class' endpoint
  fetch("/add-class", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ courseInfo }),
  })
    .then((response) => response.json())
    .then((data) => {
      // Handle the response from the server
      console.log(data.message);

      // Close the modal or perform any other necessary actions
      $("#addClassModal").modal("hide");
    })
    .catch((error) => {
      // Handle the error
      console.error("Error:", error);
    });
}

document.addEventListener("DOMContentLoaded", function () {
  // Add event listener to the body to catch all clicks
  document.body.addEventListener("click", function (event) {
    // Check if the clicked element has the class 'add-class-btn'
    if (event.target.classList.contains("add-class-btn")) {
      // Call the function to handle the button click
      handleAddClassClick(event.target);
    }
  });
});

document.addEventListener("DOMContentLoaded", function () {
  // Execute this code when the DOM is fully loaded

  // Make an AJAX call to fetch schedule data
  fetch("/get-schedule")
    .then((response) => response.json())
    .then((data) => {
      // Update the HTML with the fetched data
      updateSchedule(data);
    })
    .catch((error) => {
      console.error("Error fetching schedule data:", error);
    });
});

// Function to update the schedule HTML
function updateSchedule(data) {
  console.log("Updating schedule with data:", data);

  // Check if data is defined and is an object
  if (data && typeof data === "object") {
    // Iterate over each day and update the HTML
    Object.keys(data).forEach((day) => {
      const dayElement = document.getElementById(day);

      if (dayElement) {
        // Clear any existing content in the day element
        dayElement.innerHTML = "";

        // Check if classes is defined and an array
        if (Array.isArray(data[day])) {
          // Iterate over classes for the current day and append them to the HTML
          data[day].forEach((classIdObject) => {
            const classElement = document.createElement("div");

            // Extract the ObjectId value from the classIdObject
            const classIdString = classIdObject.$oid;

            // Fetch course information by ID
            fetch(`/get-course/${classIdString}`)
              .then((response) => response.json())
              .then((courseData) => {
                // Check if courseData is defined and contains the expected properties
                if (courseData && courseData.courseName) {
                  // Update the classElement with course information
                  classElement.innerHTML = `
                    <p>${courseData.courseName}</p>
                    <p>${classIdString}</p>
                    <!-- Add more details as needed -->
                  `;
                  dayElement.appendChild(classElement);
                } else {
                  console.error(
                    "Invalid or missing course information:",
                    courseData
                  );
                }
              })
              .catch((error) => {
                console.error("Error fetching course information:", error);
              });
          });
        } else {
          console.error("Invalid or missing 'classes' property for day:", day);
        }
      }
    });
  } else {
    console.error("Invalid or undefined data:", data);
  }
}
