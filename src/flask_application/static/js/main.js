function changeCheckboxLabel(checkBox, newLabelContent) {
    let label = document.querySelector(`label[for='${checkBox.id}']`)
    let content = label.getElementsByClassName('label-content')[0]
    content.textContent = newLabelContent
}

// Instalocker on/off
const instalockerCheckBox = document.getElementById('instalocker-start-stop')
instalockerCheckBox.addEventListener('change', function () {
    let label = document.querySelector(`label[for='${this.id}']`)
    if (this.checked) {
        $.ajax({
            url: APP_ROUTES["instalocker_bp.start"],
            type: 'POST',
        })
        label.classList.add("is-checked")
        changeCheckboxLabel(this, 'Deactivate')
    } else {
        $.ajax({
            url: APP_ROUTES["instalocker_bp.stop"],
            type: 'POST',
        })
        label.classList.remove("is-checked")
        changeCheckboxLabel(this, 'Activate')
    }
})

// TODO: show profile description when hovering a profile item
// TODO: since the set and delete form is not acting like a normal form, change this to handle the data submission in a better-practices way
// Set profile
const setProfileForm = document.getElementById('set-profile-form');
setProfileForm.addEventListener('submit', function (event) {
    // Prevent the default form submission to handle it manually.
    event.preventDefault()
    const setButton = event.submitter
    const profileName = setButton.parentElement.getAttribute('data-profile-id')
    // Submit the data with AJAX.
    $.ajax({
        url: APP_ROUTES["instalocker_bp.set_profile"],
        type: 'POST',
        data: { profile_name: profileName },
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
        url: APP_ROUTES["instalocker_bp.delete_profile"],
        type: 'POST',
        data: { profile_name: profileName },
    })
    // Delete the profile item
    deleteButton.parentElement.remove()
});

// Create profile button
const createProfileCheckbox = document.getElementById('create-profile-checkbox')
createProfileCheckbox.addEventListener('change', function () {
    const label = document.querySelector(`label[for='${this.id}']`)
    const newProfileBasicInputContainer = document.getElementById('new-profile-basic-input-container')
    const smallItemContainer = document.getElementsByClassName('small-item-container')[0]
    const mapAgentContainer = document.querySelector('#new-profile-map-agent-input-container')
    // TODO: show and hide stuff
    if (this.checked) {
        label.classList.add("is-checked")
        changeCheckboxLabel(this, 'Cancel')
        // New profile name/game-mode input field
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
        // New profile name/game-mode input field
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
        url: APP_ROUTES["instalocker_bp.create_profile"],
        type: 'POST',
        data: $(this).serialize(),
    })
    // TODO: add the profile info to the page manually to not reload the page
    // Reload the page to get the new profile from the server
    location.reload()
});