console.log("Main script started");

function changeCheckboxLabel(inputElement, labelContent) {
    let label = document.querySelector(`label[for='${inputElement.id}']`);
    let content = label.getElementsByClassName('label-content')[0];
    content.textContent = labelContent;
}

const profileDescriptions = document.querySelectorAll("[data-profile-type='description']")
let shownProfileDescription = null

// Create profile section
document.getElementById('create-profile-checkbox').addEventListener('change', function () {
    let nameField = document.getElementById('create-profile-name-field')
    let infoDiv = document.getElementById('create-profile-info')

    if (this.checked) {
        changeCheckboxLabel(this, 'Cancel');
        nameField.classList.remove('hidden');
        infoDiv.classList.remove('no-show');

        // Save the profile that was not hide and hide it
        for (element of profileDescriptions) {
            if (!element.classList.contains('no-show')) {
                shownProfileDescription = element;
                element.classList.add('no-show');
            }
        }


    } else {
        changeCheckboxLabel(this, 'Create new profile');
        nameField.classList.add('hidden');
        infoDiv.classList.add('no-show');

        // Show the profile that was not hide
        shownProfileDescription.classList.remove('no-show');
    }
});

// Select profile section
// const profile_items = document.querySelectorAll("[data-profile-type='item']")

// // Attach hover event listener to each element
// elements.forEach(element => {
//     const profileId = element.dataset.profile_id; // Get the data-profile_id value

//     element.addEventListener('mouseover', () => {
//         // Step 3: Define the behavior when the element is being hovered over
//         // Example: Remove a certain class from elements with matching profile_id
//         const elementsWithProfileId = document.querySelectorAll(`[data-profile_id="${profileId}"]:not(.profile-item)`);
//         elementsWithProfileId.forEach(el => {
//             el.classList.remove('no-show');
//         });
//     });

//     element.addEventListener('mouseout', () => {
//         // Reset the class when the mouse is no longer hovering
//         const elementsWithProfileId = document.querySelectorAll(`[data-profile_id="${profileId}"]:not(.profile-item)`);
//         elementsWithProfileId.forEach(el => {
//             el.classList.add('no-show');
//         });
//     });
// });

// Instalocker on/off section
document.getElementById('instalocker-start-stop').addEventListener('change', function () {
    if (this.checked) {
        $.ajax({
            url: APP_ROUTES["instalocker_bp.start"],
            type: 'POST',
        });
        changeCheckboxLabel(this, 'Deactivate');
    } else {
        $.ajax({
            url: APP_ROUTES["instalocker_bp.stop"],
            type: 'POST',
        });
        changeCheckboxLabel(this, 'Activate');
    }
});