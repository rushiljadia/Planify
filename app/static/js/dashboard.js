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
