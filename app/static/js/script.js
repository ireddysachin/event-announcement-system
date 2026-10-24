
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

    const bannerFile = document.getElementById("event-banner").files[0];
    let bannerResult = { object_uri: "" };

    eventMessage.textContent = "Creating event...";
    eventMessage.style.color = "black";

    try {
        // Upload the optional banner first.
        if (bannerFile) {
            eventMessage.textContent = "Uploading banner...";

            const bannerFormData = new FormData();
            bannerFormData.append("banner", bannerFile);

            const bannerResponse = await fetch("/api/banners", {
                method: "POST",
                body: bannerFormData
            });

            bannerResult = await bannerResponse.json();

            if (!bannerResponse.ok || !bannerResult.success) {
                eventMessage.textContent =
                    bannerResult.message || "Banner upload failed.";
                eventMessage.style.color = "red";
                return;
            }
        }

        // Create the event using the existing JSON API.
        const newEvent = {
            title: document.getElementById("event-title").value.trim(),
            date: document.getElementById("event-date").value,
            location: document.getElementById("event-location").value.trim(),
            description: document.getElementById("event-description").value.trim(),
            banner_uri: bannerFile ? bannerResult.object_uri : ""
        };

        eventMessage.textContent = "Saving event...";

        const response = await fetch("/api/events", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(newEvent)
        });

        const result = await response.json();

        if (response.ok && result.success) {
            createEventForm.reset();
            eventMessage.style.color = "green";
            eventMessage.textContent = "Event created successfully!";

            setTimeout(() => {
                window.location.reload();
            }, 2000);
        } else {
            eventMessage.textContent =
                result.message || "Unable to create event.";
            eventMessage.style.color = "red";
        }
    } catch (error) {
        eventMessage.textContent =
            "Unable to create event. Please try again.";
        eventMessage.style.color = "red";
        console.error("Event creation error:", error);
    }
});



