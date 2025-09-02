SERVER_HOST = "http://localhost/api/submissions";



function handleRadioChange(event) {
    const value = event.target.value;
    const multipleChoiceDiv = event.target.closest('[activity]');
    const encryptedData = multipleChoiceDiv.getAttribute("activity")

    submission = {
        "answer": value,
        "encrypted_data": encryptedData
    }

    fetch(SERVER_HOST, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(submission)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const activity_id = multipleChoiceDiv.getAttribute("activity-identifier");
        if (data['correct']) {
            multipleChoiceDiv.style.backgroundColor = "greenyellow";
            cookieStore.set(activity_id, "true");
        } else {
            multipleChoiceDiv.style.backgroundColor = "red";
            cookieStore.set(activity_id, "false");
        }

        if (data['hint']) {
            const hintParagraph = multipleChoiceDiv.querySelector('[hint]');
            hintParagraph.textContent = data['hint'];
        }

    })
    .catch(error => {
        console.error('Error:', error);
    });
}


document.querySelectorAll('input[name^="option"]').forEach(radio => {
    radio.addEventListener('change', handleRadioChange);
});


document.querySelectorAll('[activity-identifier]').forEach(async activity => {
    const cookie = await cookieStore.get(activity.getAttribute("activity-identifier"));
    if (cookie != null) {
        if (cookie.value == "true") {
            activity.style.backgroundColor = "greenyellow";
        } else if (cookie.value == "false") {
            activity.style.backgroundColor = "red";
        }
    }
});
