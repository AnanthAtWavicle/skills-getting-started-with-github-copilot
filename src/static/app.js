document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // Clear and reset activity select dropdown
      while (activitySelect.options.length > 1) {
        activitySelect.remove(1);
      }
      activitySelect.value = "";

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        const participantsHtml = details.participants.length > 0 
          ? `<ul class="participants-list">${details.participants.map(p => `<li><span class="participant-email">${p}</span> <button class="delete-btn" data-email="${p}" data-activity="${name}" title="Remove participant">🗑️</button></li>`).join('')}</ul>`
          : '<p class="no-participants">🚀 No participants yet</p>';

        activityCard.innerHTML = `
          <div class="card-header">
            <h4>${name}</h4>
            <span class="availability-badge" style="background-color: ${spotsLeft > 5 ? '#4caf50' : spotsLeft > 0 ? '#ff9800' : '#f44336'}">${spotsLeft}</span>
          </div>
          <p class="description">${details.description}</p>
          <div class="card-details">
            <p><strong>⏰ Schedule:</strong> ${details.schedule}</p>
            <p><strong>👥 Capacity:</strong> ${details.participants.length}/${details.max_participants}</p>
          </div>
          <div class="participants-section">
            <h5>📋 Participants</h5>
            ${participantsHtml}
          </div>
        `;

        activitiesList.appendChild(activityCard);

        // Add event listeners for delete buttons
        activityCard.querySelectorAll('.delete-btn').forEach(btn => {
          btn.addEventListener('click', async () => {
            const email = btn.dataset.email;
            const activity = btn.dataset.activity;

            try {
              const response = await fetch(
                `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
                {
                  method: "DELETE",
                }
              );

              if (response.ok) {
                // Refresh the activities
                fetchActivities();
              } else {
                const result = await response.json();
                alert(result.detail || "Failed to unregister");
              }
            } catch (error) {
              alert("Failed to unregister. Please try again.");
              console.error("Error unregistering:", error);
            }
          });
        });

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        // Refresh activities to show updated participants
        fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
