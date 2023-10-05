function changeCheckboxLabel(checkBox, newLabelContent) {
    let label = document.querySelector(`label[for='${checkBox.id}']`)
    let content = label.getElementsByClassName('label-content')[0]
    content.textContent = newLabelContent
}

const copyableElements = document.querySelectorAll('.copyable')
copyableElements.forEach(function (element) {
    element.addEventListener('click', function () {
        const contentToCopy = element.innerText;
        navigator.clipboard.writeText(contentToCopy);
    });
});

// ===================================================================== //
// ============================ INSTALOCKER ============================ //
// ===================================================================== //
try {
// Instalocker on/off
const instalockerCheckBox = document.getElementById('instalocker-start-stop')
instalockerCheckBox.addEventListener('change', function () {
    let label = document.querySelector(`label[for='${this.id}']`)
    if (this.checked) {
        $.ajax({
            url: APP_ROUTES.instalocker.start,
            type: 'PUT',
            success: function(data) {
                // Check if the response contains a new template (non-empty string)
                // A new template means a error message. (valorant was closed while the application is running)
                if (typeof data === 'string' && data.trim().length > 0) {
                    // If the response is a new template, reload the page
                    window.location.reload();
                }
            }
        })
        label.classList.add("is-checked")
        changeCheckboxLabel(this, 'Deactivate')
    } else {
        $.ajax({
            url: APP_ROUTES.instalocker.stop,
            type: 'PUT',
            success: function(data) {
                // Check if the response contains a new template (non-empty string)
                // A new template means a error message. (valorant was closed while the application is running)
                if (typeof data === 'string' && data.trim().length > 0) {
                    // If the response is a new template, reload the page
                    window.location.reload();
                }
            }
        })
        label.classList.remove("is-checked")
        changeCheckboxLabel(this, 'Activate')
    }
})

// TODO: since the set and delete form is not acting like a normal form, change this to handle the data submission in a better-practices way
// TODO: Do not make ajax request if trying to set a profile that is already set 
// Set profile
const setProfileForm = document.getElementById('set-profile-form');
setProfileForm.addEventListener('submit', function (event) {
    // Prevent the default form submission to handle it manually.
    event.preventDefault()
    const setButton = event.submitter
    const profileName = setButton.parentElement.getAttribute('data-profile-id')
    // Submit the data with AJAX.
    $.ajax({
        url: APP_ROUTES.instalocker.set_profile,
        type: 'PUT',
        data: { profile_name: profileName },
        success: function(data) {
            // Check if the response contains a new template (non-empty string)
            // A new template means a error message. (valorant was closed while the application is running)
            if (typeof data === 'string' && data.trim().length > 0) {
                // If the response is a new template, reload the page
                window.location.reload();
            }
        }
    })
    // Remove the is-checked class from the other buttons
    const submitButtons = document.querySelectorAll(`button[type='submit'][form='${this.id}']`);
    submitButtons.forEach(button => {
        button.classList.remove('is-checked')
    });
    // Add the is-not-display to profile descriptions
    const profileDescriptions = document.querySelectorAll(`[data-profile-type="description"]`)
    profileDescriptions.forEach(profile => {
        profile.classList.add('is-not-display')
    })
    // Add the is-checked class to the button that was just clicked
    setButton.classList.add("is-checked")
    // Remove the is-not-display class from the description of the set profile
    document.querySelectorAll(`[data-profile-id="${profileName}"][data-profile-type="description"]`)[0].classList.remove('is-not-display')
});

// Delete profile
const deleteProfileForm = document.getElementById('delete-profile-form');
deleteProfileForm.addEventListener('submit', function (event) {
    // Prevent the default form submission to handle it manually.
    event.preventDefault()
    const deleteButton = event.submitter
    const profileName = deleteButton.parentElement.getAttribute('data-profile-id')
    // Submit the data with AJAX.
    $.ajax({
        url: APP_ROUTES.instalocker.delete_profile,
        type: 'DELETE',
        data: { profile_name: profileName },
        success: function(data) {
            // Check if the response contains a new template (non-empty string)
            // A new template means a error message. (valorant was closed while the application is running)
            if (typeof data === 'string' && data.trim().length > 0) {
                // If the response is a new template, reload the page
                window.location.reload();
            }
        }
    })
    // Delete the profile item and description
    deleteButton.parentElement.remove()
    document.querySelectorAll(`[data-profile-id="${profileName}"][data-profile-type="description"]`)[0].remove()
});

// Create profile button
const createProfileCheckbox = document.getElementById('create-profile-checkbox')
createProfileCheckbox.addEventListener('change', function () {
    const label = document.querySelector(`label[for='${this.id}']`)
    const newProfileBasicInputContainer = document.getElementById('new-profile-basic-input-container')
    const smallItemContainer = document.getElementsByClassName('small-item-container')[0]
    const mapAgentContainer = document.querySelector('#new-profile-map-agent-input-container')
    if (this.checked) {
        label.classList.add("is-checked")
        changeCheckboxLabel(this, 'Cancel')
        // New profile field
        newProfileBasicInputContainer.classList.remove('is-hidden')
        // Disable profile buttons and hide descriptions
        smallItemContainer.querySelectorAll('button').forEach(button => {
            button.setAttribute("disabled", "disabled")
        })
        const profileDescriptions = document.querySelectorAll('[data-profile-type="description"]')
        profileDescriptions.forEach(profile => {
            profile.classList.add('is-not-display')
        })
        // Show map-agent fields
        mapAgentContainer.classList.remove('is-not-display')

    } else {
        label.classList.remove("is-checked")
        changeCheckboxLabel(this, 'Create new profile')
        // New profile field
        newProfileBasicInputContainer.classList.add('is-hidden')
        // Enable profile buttons and show the selected profile description
        smallItemContainer.querySelectorAll('button').forEach(button => {
            button.removeAttribute("disabled")
            if (button.classList.contains('is-checked')) {
                let profileId = button.parentElement.getAttribute('data-profile-id')
                let ProfileDescription = document.querySelectorAll(`[data-profile-id="${profileId}"][data-profile-type="description"]`)[0]
                ProfileDescription.classList.remove('is-not-display')
            }
        })
        // Hide map-agent fields
        mapAgentContainer.classList.add('is-not-display')
    }
})

// Create profile form
const newProfileForm = document.getElementById('new-profile-form');
newProfileForm.addEventListener('submit', function (event) {
    // Prevent the default form submission to handle it manually.
    event.preventDefault()
    // Submit the data with AJAX.
    $.ajax({
        url: APP_ROUTES.instalocker.create_profile,
        type: 'POST',
        data: $(this).serialize(),
        success: function(data) {
            // Check if the response contains a new template (non-empty string)
            // A new template means a error message. (valorant was closed while the application is running)
            if (typeof data === 'string' && data.trim().length > 0) {
                // If the response is a new template, reload the page
                window.location.reload();
            }
        }
    })
    // TODO: add the profile info to the page manually to not reload the page
    // Reload the page to get the new profile from the server
    location.reload()
});

// Delays
document.getElementById("set-select-delay-form").addEventListener("submit", function(event) {
    event.preventDefault();
});
const selectDelayInput = document.getElementById('select-delay')
selectDelayInput.addEventListener('input', function (event) {
    if (event.target.value === "" || isNaN(event.target.value)) {
        event.target.value = 0
    }
    let delay = parseInt(event.target.value, 10)
    event.target.value = delay
    if (delay < 0) {
        event.target.value = 0
        delay = 0
    }
    if (delay > 30) {
        event.target.value = 30
        delay = 30
    }
    if (delay >= 0 && delay <= 30 && !isNaN(delay)) {
        console.log()
        $.ajax({
            url: APP_ROUTES.instalocker.set_select_delay,
            type: 'PUT',
            data: { "delay": delay },
            success: function(data) {
                // Check if the response contains a new template (non-empty string)
                // A new template means a error message. (valorant was closed while the application is running)
                if (typeof data === 'string' && data.trim().length > 0) {
                    // If the response is a new template, reload the page
                    window.location.reload();
                }
            }
        })
    } 
})

document.getElementById("set-lock-delay-form").addEventListener("submit", function(event) {
    event.preventDefault();
});
const lockDelayInput = document.getElementById('lock-delay')
lockDelayInput.addEventListener('input', function (event) {
    if (event.target.value === "" || isNaN(event.target.value)) {
        event.target.value = 0
    }
    let delay = parseInt(event.target.value, 10)
    event.target.value = delay
    if (delay < 0) {
        event.target.value = 0
        delay = 0
    }
    if (delay > 30) {
        event.target.value = 30
        delay = 30
    }
    if (delay >= 0 && delay <= 30 && !isNaN(delay)) {
        $.ajax({
            url: APP_ROUTES.instalocker.set_lock_delay,
            type: 'PUT',
            data: { "delay": delay },
            success: function(data) {
                // Check if the response contains a new template (non-empty string)
                // A new template means a error message. (valorant was closed while the application is running)
                if (typeof data === 'string' && data.trim().length > 0) {
                    // If the response is a new template, reload the page
                    window.location.reload();
                }
            }
        })
    } 
})
} catch (error) {
}
// ===================================================================== //
// ============================ END INSTALOCKER ======================== //
// ===================================================================== //


// ===================================================================== //
// ============================= STREAM HUNTER ========================= //
// ===================================================================== //
try {
const huntButton = document.getElementById('hunt');
huntButton.addEventListener('click', function () {
    $.ajax({
        url: APP_ROUTES.stream_hunter.streams,
        type: 'GET',
        data: {},
        success: function(data) {
            console.log(data)
            // Construct the streams container with the data
            const container = document.getElementById('streams-container');
            container.innerHTML = '';
            for (const name in data) {
                console.log(name)
                const playerDiv = document.createElement('div');
                playerDiv.classList.add('player');

                const nameDiv = document.createElement('div');
                nameDiv.classList.add('name');
                nameDiv.innerHTML = `<strong>${name}</strong>`;
                playerDiv.appendChild(nameDiv);

                const streamsUl = document.createElement('ul');
                streamsUl.classList.add('streams');

                if (data[name].length === 0) {
                    const noStreamsLi = document.createElement('li');
                    noStreamsLi.textContent = 'No streams found';
                    streamsUl.appendChild(noStreamsLi);
                } else {
                    for (const stream of data[name]) {
                        const streamLi = document.createElement('li');
                        streamLi.classList.add('copyable');
                        streamLi.textContent = stream;
                        streamsUl.appendChild(streamLi);
                    }
                }
                playerDiv.appendChild(streamsUl);
                container.appendChild(playerDiv);
            }
        }
    })
});
} catch (error) {
}