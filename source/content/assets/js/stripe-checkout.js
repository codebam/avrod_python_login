console.log("script loaded.")

var stripe = Stripe('pk_test_FAFu3glBDqdKrdvJNOiF94iZ00LEThelHv');
var button = document.getElementById('monthly-btn');

button.addEventListener('click', function() {
  stripe.redirectToCheckout({
    sessionId: session_id
  }).then(function (result) {
    console.log(result.error.message)
  });
});
