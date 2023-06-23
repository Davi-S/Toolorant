console.log("Main script started");


// Instalocker on/off
document.getElementById('start/stop_instalocker').addEventListener('change', function () {
    if (this.checked) {
        $.ajax({
            url: APP_ROUTES["instalocker_bp.start"],
            type: 'POST',
        });
    } else {
        $.ajax({
            url: APP_ROUTES["instalocker_bp.stop"],
            type: 'POST',
        });
    }
});
