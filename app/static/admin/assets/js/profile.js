function updateProfile() {
    var RegisterForm = document.getElementById('RegisterForm');
    var ProfileUpdateForm = new FormData(ProfileUpdateForm);

    if (ProfileUpdateForm.get('name').trim() === '') {
        iziToast.error({
            title: 'Validation Error',
            message: 'Please enter your name.',
            position: 'topRight',
            timeout: 3000
        });
        return false;
    }

    var xhr = new XMLHttpRequest();
    xhr.open('POST', ProfileUpdateForm.action, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        if (xhr.status === 200 && xhr.response.success) {
            iziToast.success({
                title: 'Profile Update',
                message: 'Successfully Profile Updated!',
                position: 'topRight',
                timeout: 3000
            });

            form.reset();
        } else {
            iziToast.error({
                title: 'Profile Update Failed',
                message: 'failed to update profile',
                position: 'topRight',
                timeout: 3000
            });
        }
    };
    xhr.send(new URLSearchParams(ProfileUpdateForm).toString());

    return false;
}
