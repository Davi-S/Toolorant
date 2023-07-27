console.log("Main script started")

function changeCheckboxLabel(checkBox, newLabelContent) {
    let label = document.querySelector(`label[for='${checkBox.id}']`)
    let content = label.getElementsByClassName('label-content')[0]
    content.textContent = newLabelContent
}

// const profileDescriptions = document.querySelectorAll("[data-profile-type='description']")
// let shownProfileDescription = null

// // Create profile section
// document.getElementById('create-profile-checkbox').addEventListener('change', function () {
//     let nameField = document.getElementById('create-profile-name-field')
//     let infoDiv = document.getElementById('create-profile-info')

//     if (this.checked) {
//         changeCheckboxLabel(this, 'Cancel')
//         nameField.classList.remove('hidden')
//         infoDiv.classList.remove('no-show')

//         // Save the profile that was not hide and hide it
//         for (element of profileDescriptions) {
//             if (!element.classList.contains('no-show')) {
//                 shownProfileDescription = element
//                 element.classList.add('no-show')
//             }
//         }


//     } else {
//         changeCheckboxLabel(this, 'Create new profile')
//         nameField.classList.add('hidden')
//         infoDiv.classList.add('no-show')

//         // Show the profile that was not hide
//         shownProfileDescription.classList.remove('no-show')
//     }
// })

// Select profile section
// const profile_items = document.querySelectorAll("[data-profile-type='item']")

// // Attach hover event listener to each element
// elements.forEach(element => {
//     const profileId = element.dataset.profile_id // Get the data-profile_id value

//     element.addEventListener('mouseover', () => {
//         // Step 3: Define the behavior when the element is being hovered over
//         // Example: Remove a certain class from elements with matching profile_id
//         const elementsWithProfileId = document.querySelectorAll(`[data-profile_id="${profileId}"]:not(.profile-item)`)
//         elementsWithProfileId.forEach(el => {
//             el.classList.remove('no-show')
//         })
//     })

//     element.addEventListener('mouseout', () => {
//         // Reset the class when the mouse is no longer hovering
//         const elementsWithProfileId = document.querySelectorAll(`[data-profile_id="${profileId}"]:not(.profile-item)`)
//         elementsWithProfileId.forEach(el => {
//             el.classList.add('no-show')
//         })
//     })
// })

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

// TODO: since the set and delete form is not acting like a normal form, change this to handle the data submission in a better-practices way
// Set profile
const setProfileForm = document.getElementById('set-profile-form');
setProfileForm.addEventListener('submit', function (event) {
    // Prevent the default form submission to handle it manually.
    event.preventDefault()
    const profileName = event.submitter.parentElement.getAttribute('data-profile-id')
    // Submit the data with AJAX.
    $.ajax({
        url: APP_ROUTES["instalocker_bp.set_profile"],
        type: 'POST',
        data: { profile_name: profileName },
    })

    // Handle element classes
    // Remove the is-checked class from the other buttons
    const submitButtons = document.querySelectorAll(`button[type='submit'][form='${event.target.id}']`);
    submitButtons.forEach(button => {
        button.classList.remove('is-checked')
    });
    // Add the is-checked class to the button that was just clicked
    event.submitter.classList.add("is-checked")
});

// Delete profile
const deleteProfile = document.getElementById('delete-profile-form');
deleteProfile.addEventListener('submit', function (event) {
    // Prevent the default form submission to handle it manually.
    event.preventDefault()
    const profileName = event.submitter.parentElement.getAttribute('data-profile-id')
    // Submit the data with AJAX.
    $.ajax({
        url: APP_ROUTES["instalocker_bp.delete_profile"],
        type: 'POST',
        data: { profile_name: profileName },
    })
    // Reload the page
    location.reload();
});

// Create profile
const createProfileCheckbox = document.getElementById('create-profile-checkbox')
createProfileCheckbox.addEventListener('change', function () {
    let label = document.querySelector(`label[for='${this.id}']`)
    if (this.checked) {
        label.classList.add("is-checked")
        changeCheckboxLabel(this, 'Cancel')
    } else {
        label.classList.remove("is-checked")
        changeCheckboxLabel(this, 'Create new profile')
    }
})