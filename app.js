// Get the form element
const form = document.querySelector('form');

// Listen for form submission
form.addEventListener('submit', async (event) => {
  // Prevent the form from submitting
  event.preventDefault();

  // Get the input values
  const username = form.elements.username.value;
  const password = form.elements.password.value;

  try {
    // Send a POST request to the server with the user's credentials
    const response = await fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, password })
    });

    // Parse the response
    const data = await response.json();

    // Check if the login was successful
    if (data.success) {
      // Redirect the user to the home page
      window.location.href = '/home';
    } else {
      // Display an error message
      alert('Invalid credentials');
    }
  } catch (error) {
    console.error(error);
  }
});