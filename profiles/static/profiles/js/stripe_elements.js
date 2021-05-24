
var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
var stripe_secret_key = $('#id_stripe_secret_key').text().slice(1, -1);
var stripe = Stripe(stripe_public_key);
var elements = stripe.elements({
    fonts: [
        {
          cssSrc: 'https://fonts.googleapis.com/css2?family=Oswald&display=swap'
        }
    ]
});

var card = elements.create('card', {
    style: {
        base: {
            color: '#000',
            fontFamily: 'Oswald, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#aab7c4'
            }
        },
        invalid: {
            color: '#FF7C1F',
            iconColor: '#FF7C1F'
        },
    },
});

card.mount('#card-element');

// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// NEW SUBSCRIPTION

// Create a token or display an error when the form is submitted.
var form = document.getElementById('membership_form');
form.addEventListener('submit', function(event) {
    event.preventDefault();
    card.update({'disabled': true});
    $('#submit-button').attr('disabled', true);
    $('#membership_form').fadeToggle(100);
    $('#loading').fadeToggle(100);

  stripe.createToken(card).then(function(result) {
    if (result.error) {
      // Inform the customer that there was an error.
      var errorElement = document.getElementById('card-errors');
      errorElement.textContent = result.error.message;
      $('#membership_form').fadeToggle(100);
      $('#loading').fadeToggle(100);
      card.update({ 'disabled': false});
      $('#submit-button').attr('disabled', false);
    } else {
      // Send the token to your server.
      stripeTokenHandler(result.token);
    }
  });
});

function stripeTokenHandler(token) {
    // Insert the token ID into the form so it gets submitted to the server
    var form = document.getElementById('membership_form');
    var hiddenInput = document.createElement('input');
    hiddenInput.setAttribute('type', 'hidden');
    hiddenInput.setAttribute('name', 'stripeToken');
    hiddenInput.setAttribute('value', token.id);
    form.appendChild(hiddenInput);
    // Submit the form
    form.submit();
    }
