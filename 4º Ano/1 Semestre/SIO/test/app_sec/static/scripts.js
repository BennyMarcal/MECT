// Path: app_sec/static/scripts.js
function showPassword(x) {
  var e = document.getElementById(x);
  if (e.type === "password") {
    e.type = "text";
  } else {
    e.type = "password";
  }
}

function validateEmail() {
  var emailInput = document.getElementById("email");
  var emailValue = emailInput.value;
  var isValid = /^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$/.test(
    emailValue
  );

  if (!isValid) {
    alert("Please enter a valid email address (e.g., yourname@example.com).");
    emailInput.focus();
    return false;
  }
  return true;
}

function showPassword(x) {
  var e = document.getElementById(x);
  if (e.type === "password") {
    e.type = "text";
  } else {
    e.type = "password";
  }
}

function calculatePasswordStrength(password) {
  var upperCase = /[A-Z]/g;
  var numeric = /[0-9]/g;
  var special = /[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]/g;

  if (
    password.length > 12 &&
    upperCase.test(password) &&
    numeric.test(password) &&
    special.test(password)
  ) {
    return { strength: "Strong", color: "green" };
  }
  if (
    password.length > 12 &&
    (upperCase.test(password) ||
      numeric.test(password) ||
      special.test(password))
  ) {
    return { strength: "Moderate", color: "orange" };
  } else {
    return { strength: "Weak", color: "red" };
  }
}

document.getElementById("password").addEventListener("input", function () {
  var password = this.value;
  var obj = calculatePasswordStrength(password);
  document.getElementById("password-strength").innerText =
    "Password Strength: " + obj.strength;
  document.getElementById("password-strength").style.color = obj.color;
});
