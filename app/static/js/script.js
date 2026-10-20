
const subscribeForm = document.getElementById("subscribe-form");
const message = document.getElementById("message");

subscribeForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();

    if (!email) {
        message.textContent = "Please enter your email address.";
        return;
    }

    try {
        const response = await fetch("/subscribe", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email: email })
        });

        const result = await response.json();

        message.textContent = result.message;

        if (result.success) {
            subscribeForm.reset();
        }
    } catch (error) {
        message.textContent =
            "Unable to subscribe. Please try again.";
        console.error("Subscription error:", error);
    }
});


const createEventForm = document.getElementById("create-event-form");
const eventMessage = document.getElementById("event-message");

createEventForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const newEvent = {
        title: document.getElementById("event-title").value.trim(),
        date: document.getElementById("event-date").value,
        location: document.getElementById("event-location").value.trim(),
        description: document.getElementById("event-description").value.trim()
    };

    eventMessage.textContent = "Creating event...";

    try {
        const response = await fetch("/api/events", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(newEvent)
        });

        const result = await response.json();

        eventMessage.textContent = result.message ||
            (result.success ? "Event created successfully!" : "Unable to create event.");

       if (response.ok && result.success) {
            createEventForm.reset();

          // Show the success message before refreshing.
          eventMessage.style.color = "green";
          eventMessage.textContent = "Event created successfully!";

         setTimeout(() => {
         window.location.reload();
       }, 2000);
       } else {
         eventMessage.style.color = "red";
       }

    } catch (error) {
        eventMessage.textContent = "Unable to create event. Please try again.";
        console.error("Event creation error:", error);
    }
});


