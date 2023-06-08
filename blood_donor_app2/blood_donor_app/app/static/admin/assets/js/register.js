function validateForm() {
  let name = document.getElementById("name").value;
  let age = document.getElementById("age").value;
  let contact_number = document.getElementById("contact_number").value;
  let address = document.getElementById("address").value;
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;
  let phoneRegex = /^(?:\+|00)?230(\d{8})$/;

  if (name == ""){
    iziToast.error({
      title: 'Error',
      message: 'Name is required',
    });
  return false
  }
  if (age == ""){
    iziToast.error({
      title: 'Error',
      message: 'Age is required',
    });
  return false
  }
  if (contact_number == ""){
    iziToast.error({
      title: 'Error',
      message: 'Contact Number is required',
    });
  return false
  }
   if (address == ""){
    iziToast.error({
      title: 'Error',
      message: 'address is required',
    });
  return false
  }


  if (username == "") {
    iziToast.error({
      title: 'Error',
      message: 'Username is required',
    });
    return false;
  }
  if (password == "") {
    iziToast.error({
      title: 'Error',
      message: 'Password is required',
    });
    return false;
  }  if (password.length < 8) {
    iziToast.error({
      title: 'Error',
      message: 'Password must be at least 8 characters long.',
    });
    return false;
  }
  if (!phoneRegex.test(contact_number))
            {
                iziToast.error(
                    {
                        title: 'Error',
                        message: "Contact number must be a valid Mauritius phone number",
                    }
                );
                return false;
            }
  return true;
}

