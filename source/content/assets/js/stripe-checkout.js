console.log("script loaded.")

var stripe = Stripe('pk_test_FAFu3glBDqdKrdvJNOiF94iZ00LEThelHv');
var elements = stripe.elements();

var style = {
  base: {
    color: "#32325d",
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: "antialiased",
    fontSize: "16px",
    "::placeholder": {
      color: "#aab7c4"
    }
  },
  invalid: {
    color: "#fa755a",
    iconColor: "#fa755a"
  }
};


var cardElement = elements.create("card", { style: style });
cardElement.mount("#card-element");

cardElement.addEventListener('change', ({error}) => {
  const displayError = document.getElementById('card-errors');
  if (error) {
    displayError.textContent = error.message;
  } else {
    displayError.textContent = '';
  }
});

const form = document.getElementById('subscription-form');

form.addEventListener('submit', async (event) => {
  // We don't want to let default form submission happen here,
  // which would refresh the page.
  event.preventDefault();

  const result = await stripe.createPaymentMethod({
    type: 'card',
    card: cardElement,
    billing_details: {
      email: 'jenny.rosen@example.com',
    },
  })

  stripePaymentMethodHandler(result);
});

const stripePaymentMethodHandler = async (result) => {
  if (result.error) {
    // Show error in payment form
  } else {
    // Otherwise send paymentMethod.id to your server
    const res = await fetch('/create-customer', {
      method: 'post',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        email: 'jenny.rosen@example.com',
        payment_method: result.paymentMethod.id
      }),
    });

    // The customer has been created
    const customer = await res.json();
  }
}

// const form = document.getElementById('subscription-form');

// form.addEventListener('submit', async (event) => {
//   // We don't want to let default form submission happen here,
//   // which would refresh the page.
//   event.preventDefault();

//   const result = await stripe.createPaymentMethod({
//     type: 'card',
//     card: cardElement,
//     billing_details: {
//       email: 'jenny.rosen@example.com',
//     },
//   })

//   stripePaymentMethodHandler(result);
// });
