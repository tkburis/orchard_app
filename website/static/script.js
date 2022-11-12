function getCoords() {
    const options = {
        enableHighAccuracy: true,
        timeout: Infinity,
        maximumAge: 0
    }
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(getSuccess, getError, options)
    } else {
        alert("Geolocation is not supported by your browser")
    }
}

function getSuccess(pos) {
    document.getElementById("coordLat").value = pos.coords.latitude
    document.getElementById("coordLong").value = pos.coords.longitude
}

function getError() {
    alert("Please allow this page to access your location")
}

function deleteTree(treeId) {
    fetch('/admin/delete-tree', {
        method: 'POST',
        body: JSON.stringify({treeId: treeId})
    }).then((_res) => {
        window.location.href = "/admin";
    });
}

// Form validation
(() => {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
        }

        form.classList.add('was-validated')
        }, false)
    })
})()
