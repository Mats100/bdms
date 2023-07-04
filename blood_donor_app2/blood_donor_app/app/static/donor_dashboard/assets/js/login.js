function validateForm() {
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;
  if (username === "") {
    iziToast.error({
      title: 'Error',
      message: 'Username is required',
      position: 'topRight'
  });
    return false;
  }
  if (password === "") {
    iziToast.error({
      title: 'Error',
      message: 'Password is required',
      position: 'topRight'
  });
    return false;
  }
}