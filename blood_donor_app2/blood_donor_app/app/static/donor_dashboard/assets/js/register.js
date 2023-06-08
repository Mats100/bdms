
    function validateForm(){
    var name = document.getElementById("name").value;
    let age = document.getElementById("age").value;
    let contactNumber = document.getElementById("contact_number").value;
    let email = document.getElementById("email").value;
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let address = document.getElementById("address").value;
    let weight = document.getElementById("weight").value;
    let bloodType = document.getElementById("blood_type").value;
    let pulseRate = document.getElementById("pulse_rate").value;
    let haemoglobin = document.getElementById("haemoglobin").value;
    let bloodPressure = document.getElementById("blood_pressure").value;
    let temperature = document.getElementById("temperature").value;
    const phoneRegex = /^(?:\+|00)?230(\d{8})$/;

        if (name === "" || age === "" || contactNumber === "" || email === "" || username === "" || password === "" || address === "" ||
    weight === "" || bloodType === "" || pulseRate === "" || haemoglobin === "" || bloodPressure === "" || temperature === "") {
    iziToast.error({
      title: 'Error',
      message: 'Fields are required',
    });
  return false
  }
    if (isNaN(age) || age < 18 || age > 65) {
    iziToast.error(
        {
          title: 'Error',
          message: 'Age must be between 18 and 65',
        }
    );
    return false;
}
        if (!phoneRegex.test(contactNumber))
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
