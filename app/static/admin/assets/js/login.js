function validateForm() {
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;
  if (username === "") {
    iziToast.error({
      title: 'Error',
      message: 'Username is required',
        location:'TopRight'
  });
    return false;
  }
  if (password === "") {
    iziToast.error({
      title: 'Error',
      message: 'Password is required',
        location:'TopRight'
  });
    return false;
  }
   var errorFlashMessage = document.querySelector('.flash-message.error');
    if (errorFlashMessage) {
        iziToast.error({
            title: 'Error',
            message: errorFlashMessage.textContent,
            position: 'topRight',
            timeout: 5000,
            progressBarColor: '#dc3545',
            messageColor: '#ffffff',
            backgroundColor: '#dc3545',
            theme: 'dark',
        });
        return false;
    }
    return true;
}