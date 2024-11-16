document.getElementById("payment-form").addEventListener("submit", function (e) {
    e.preventDefault(); // Prevent form submission
  
    const firstName = document.getElementById("first-name").value.trim();
    const lastName = document.getElementById("last-name").value.trim();
    const phoneNumber = document.getElementById("phone-number").value.trim();
    const email = document.getElementById("email").value.trim();
    const visaType = document.getElementById("visa-type").value;
    const cardType = document.getElementById("card-type").value;
    const cardNumber = document.getElementById("card-number").value.trim();
    const nameOnCard = document.getElementById("name-on-card").value.trim();
    const cvv = document.getElementById("cvv").value.trim();
  
    if (!firstName || !lastName || !phoneNumber || !email || !visaType || !cardType || !cardNumber || !nameOnCard || !cvv) {
      alert("Please fill out all fields.");
      return;
    }
  
    alert(`Payment Successful!\nName: ${firstName} ${lastName}\nVisa Type: ${visaType}\nCard Type: ${cardType}`);
  });
  