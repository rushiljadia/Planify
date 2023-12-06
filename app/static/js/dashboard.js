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

  // Check if data is defined and iterable
  if (data && Array.isArray(data)) {
    // Iterate over each day and update the HTML
    data.forEach((dayData) => {
      // Get the day's HTML element by ID
      const dayElement = document.getElementById(`${dayData.day}-schedule`);

      if (dayElement) {
        // Clear any existing content in the day element
        dayElement.innerHTML = `
          <div class="col border text-center" style="width: 50px;">
            <h3>${dayData.day}</h3>
          </div>
        `;

        // Iterate over classes for the current day and append them to the HTML
        if (Array.isArray(dayData.classes)) {
          dayData.classes.forEach((classInfo) => {
            const classElement = document.createElement("div");
            classElement.className = "col";

            // Fetch course information by ID
            fetch(`/get-course/${classInfo._id}`)
              .then((response) => response.json())
              .then((courseData) => {
                // Update the classElement with course information
                classElement.innerHTML = `
                  <div class="card" style="width: 18rem;">
                    <div class="card-body">
                      <h5 class="card-title">${courseData.courseCode}</h5>
                      <h6 class="card-subtitle mb-2 text-body-secondary">
                        ${courseData.courseName} 
                      </h6>
                      <p class="card-text">${courseData.coursePlace}</p> 
                      <p class="card-text">${courseData.startTime} - ${courseData.endTime}</p> 
                    </div>
                  </div>
                `;
                dayElement.appendChild(classElement);
              })
              .catch((error) => {
                console.error("Error fetching course information:", error);
              });
          });
        }
      }
    });
  } else {
    console.error("Invalid or undefined data:", data);
  }
}
