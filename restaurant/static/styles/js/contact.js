// Handle form submission (optional feature)
document.getElementById('contact-form').addEventListener('submit', function (event) {
    event.preventDefault();
  
    const name = document.getElementById('name').value;
    const number = document.getElementById('number').value;
    const email = document.getElementById('email').value;
    const reason = document.getElementById('reason').value;
    const message = document.getElementById('message').value;
  
    if (name && number && email && reason && message) {
      alert(`Thank you, ${name}! Your message has been sent.`);
      console.log('alerted');
      this.reset();
    } else {
      alert('Please fill out all fields before submitting.');
    }
  });
  