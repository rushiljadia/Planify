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

// document.addEventListener("DOMContentLoaded", function () {
//   var searchInput = document.getElementById("search-input");
//   var classSection = document.getElementById("class-cards-container");

//   searchInput.addEventListener("focus", function () {
//     classSection.style.display = "block";
//   });

//   searchInput.addEventListener("blur", function () {
//     classSection.style.display = "none";
//   });
// });

// Function to handle button click
function handleAddClassClick(button) {
  const loadingAnimation = document.getElementById("loadingAnimation");
  loadingAnimation.style.display = "flex";

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

      // Hide the loading animation before reloading the page
      loadingAnimation.style.display = "none";

      location.reload();

      // Close the modal or perform any other necessary actions
      $("#addClassModal").modal("hide");
    })
    .catch((error) => {
      // Hide the loading animation in case of an error
      loadingAnimation.style.display = "none";
      // Handle the error
      console.error("Error:", error);
    });
}

//Handles schedule selector
function updateDropdown(selectedOption) {
  // Update the button text with the selected option
  $('#dropdownMenuButton').text(selectedOption);
}

// Handles the removal of classes
function removeClass(button) {
  const classId = button.getAttribute("data-class-id");
  console.log(classId);
  var answer = confirm("Are You sure you would like to remove this course?");

  if (answer) {
    const loadingAnimation = document.getElementById("loadingAnimation");
    loadingAnimation.style.display = "flex";
    // Send a request to the server to remove the class
    fetch("/remove-class", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ classId }),
    })
      .then((response) => response.json())
      .then((data) => {
        // Handle the response from the server
        console.log(data.message);

        // Reload the page after removing the class
        location.reload();

        loadingAnimation.style.display = "none";
      })
      .catch((error) => {
        // Handle the error
        console.error("Error:", error);
        // Close the loading screen in case of an error
        loadingAnimation.style.display = "none";
      });
    alert("Course Removed");
  }
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
      // Update the HTML with the fetched data and trigger geocoding
      updateScheduleAndGeocode(data);
    })
    .catch((error) => {
      console.error("Error fetching schedule data:", error);
    });
});

function formatTime(timeString) {
  const [hours, minutes] = timeString.split(":");
  let formattedHours = parseInt(hours);
  let period = "AM";

  if (formattedHours >= 12) {
    period = "PM";
    if (formattedHours > 12) {
      formattedHours -= 12;
    }
  }

  return `${formattedHours}:${minutes} ${period}`;
}

// For formatting times
function str_pad_left(string, pad, length) {
  return (new Array(length + 1).join(pad) + string).slice(-length);
}

function calculateTimeDifference(endTime1, startTime2) {
  const [hours1, minutes1] = endTime1.split(":").map(Number);
  const [hours2, minutes2] = startTime2.split(":").map(Number);

  const time1 = hours1 * 60 + minutes1;
  const time2 = hours2 * 60 + minutes2;

  return time2 - time1;
}

function timeStringToFloat(time) {
  var hoursMinutes = time.split(/[.:]/);
  var hours = parseInt(hoursMinutes[0], 10);
  var minutes = hoursMinutes[1] ? parseInt(hoursMinutes[1], 10) : 0;
  return hours + minutes / 60;
}

async function updateScheduleAndGeocode(data) {
  // Day mappings
  const dayMappings = {
    M: "Monday",
    T: "Tuesday",
    W: "Wednesday",
    R: "Thursday",
    F: "Friday",
  };

  // Check if data is defined and iterable
  if (data && Array.isArray(data)) {
    // Iterate over each day and update the HTML
    data.forEach(async (dayData) => {
      // Get the day's HTML element by ID
      const dayElement = document.getElementById(`${dayData.day}-schedule`);

      if (dayElement) {
        // Clear any existing content in the day element
        dayElement.innerHTML = `
            <div id="content" class="text-center">${
              dayMappings[dayData.day]
            }</div>
          `;

        // Create a single ul element for the day
        const daySchedule = document.createElement("ul");
        daySchedule.className = "timeline-1 text-black";

        // Sort the classes within each day based on startTime
        const sortedClasses = dayData.classes.sort((a, b) => {
          return a.startTime.localeCompare(b.startTime);
        });

        // Iterate over sorted classes for the current day and append them to the ul
        for (let i = 0; i < sortedClasses.length; i++) {
          const classInfo = sortedClasses[i];

          // Calculate the time between the end of class one and the start of class two

          // Create an li element for each class
          const classElement = document.createElement("li");
          classElement.className = "event";
          classElement.setAttribute(
            "data-date",
            `${formatTime(classInfo.startTime)} - ${formatTime(
              classInfo.endTime
            )}`
          );

          // Update the li element with course information
          classElement.innerHTML = `
              <h4 class="mb-3">${classInfo.courseCode}</h4>
              <small>${classInfo.courseName}</small>
              <hr />
              <button type="button" class="btn btn-secondary btn-sm remove-class-btn" data-bs-toggle="tooltip" data-bs-placement="right" title="Remove class" onClick="removeClass(this)" data-class-id="${classInfo._id}">
              X
              </button>
          `;

          // If there is a previous class, calculate and display distance
          if (i > 0) {
            const info = await calculateDistance(
              classInfo.coursePlace,
              sortedClasses[i - 1].coursePlace
            );

            const mins = Math.floor(info[1] / 60);
            const secs = info[1] - mins * 60;
            const finalTime =
              str_pad_left(mins, "0", 2) + ":" + str_pad_left(secs, "0", 2);

            classElement.setAttribute(
              "data-distance",
              `${info[0].toFixed(2)} mi`
            );
            classElement.setAttribute("data-time", `${finalTime} mins`);

            const walkTime = timeStringToFloat(finalTime);

            const endClassOne = timeStringToFloat(sortedClasses[i - 1].endTime);
            const startCurrClass = timeStringToFloat(classInfo.startTime);

            const timeDiff = startCurrClass - endClassOne;

            var timeInfo = "";

            if (classInfo.coursePlace === sortedClasses[i - 1].coursePlace) {
              timeInfo = "Same Place";
              classElement.style.color = "Blue";
            } else if (walkTime - timeDiff > 5) {
              timeInfo = "Plenty of time!";
              classElement.style.color = "Green";
            } else if (walkTime - timeDiff <= 5 && walkTime - timeDiff > 1) {
              timeInfo = "Somewhat Risky";
              classElement.style.color = "Purple";
            } else {
              timeInfo = "Not Possible!";
              classElement.style.color = "red";
            }

            classElement.setAttribute("data-info", `${timeInfo}`);
          }

          // Append the li to the day's ul
          daySchedule.appendChild(classElement);
        }

        // Append the ul to the day's content
        dayElement.querySelector("#content").appendChild(daySchedule);

        // Trigger geocoding for the current day's classes
        const geocodedResults = await geocodeAllAddresses(sortedClasses);
        console.log(
          `Geocoded Results for ${dayMappings[dayData.day]}:`,
          geocodedResults
        );
      }
    });
  } else {
    console.error("Invalid or undefined data:", data);
  }
}

const TOKEN =
  "pk.eyJ1Ijoia2FwaGVscHMzMyIsImEiOiJjbG9xOHJoczEwZzd3MmttY2E1azIxMDE2In0.6aYFPziyzO_qDoSY4zIpIQ";

// API USAGE

// Function to geocode addresses
async function geocodeAllAddresses(scheduleData) {
  const geocodedResults = await Promise.all(
    scheduleData.map(async (classInfo) => {
      const address = classInfo.coursePlace;

      if (!address) {
        console.error(`Address not found for place: ${address}`);
        return null;
      }

      const coordinates = await geocodeAddress(address);

      if (coordinates) {
        // Merge the geocoded coordinates with the class information
        return { ...classInfo, coordinates };
      } else {
        return null;
      }
    })
  );

  return geocodedResults.filter((result) => result !== null);
}

async function geocodeAddress(address) {
  const apiKey = TOKEN;
  const endPoint = `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(
    address
  )}.json?access_token=${apiKey}`;

  try {
    const response = await fetch(endPoint);
    const data = await response.json();

    if (data.features && data.features.length > 0) {
      // Extract the first result (assuming it's the most relevant)
      const [longitude, latitude] = data.features[0].center;
      return { latitude, longitude };
    } else {
      console.error("Geocoding failed. No results found.");
      return null;
    }
  } catch (error) {
    console.error("Error during geocoding:", error);
    return null;
  }
}

async function calculateDistance(originPlace, destinationPlace) {
  const apiKey = TOKEN;
  const originAddress = originPlace;
  const destinationAddress = destinationPlace;

  if (!originAddress || !destinationAddress) {
    console.error("Origin or destination address not found.");
    return null;
  }

  const originCoordinates = await geocodeAddress(originAddress);
  const destinationCoordinates = await geocodeAddress(destinationAddress);

  if (!originCoordinates || !destinationCoordinates) {
    console.error("Geocoding failed for origin or destination.");
    return null;
  }

  const endpoint = `https://api.mapbox.com/directions/v5/mapbox/walking/${originCoordinates.longitude},${originCoordinates.latitude};${destinationCoordinates.longitude},${destinationCoordinates.latitude}?geometries=geojson&access_token=${apiKey}`;

  try {
    const response = await fetch(endpoint);
    const data = await response.json();

    if (data.routes && data.routes.length > 0) {
      // Extract the distance from the response
      const distance = data.routes[0].distance / 1609; // Convert meters to miles
      const duration = data.routes[0].duration; // Number of seconds
      return [distance, duration];
    } else {
      console.error("Directions API failed. No routes found.");
      return null;
    }
  } catch (error) {
    console.error("Error during Directions API request:", error);
    return null;
  }
}
