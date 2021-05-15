
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