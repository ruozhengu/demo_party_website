var dropin;
var payBtn = document.getElementById('pay-btn');
var nonceGroup = document.querySelector('.nonce-group');
var nonceInput = document.querySelector('.nonce-group input');
var nonceSpan = document.querySelector('.nonce-group span');
var payGroup = document.querySelector('.pay-group');
var billingFields = [
  'invittes',
  'starttime',
  'closetime',
  'budgets',
  'deliverytime',
  'customization',
].reduce(function (fields, fieldName) {
  var field = fields[fieldName] = {
    input: document.getElementById(fieldName),
    help: document.getElementById('help-' + fieldName)
  };

  field.input.addEventListener('focus', function() {
    clearFieldValidations(field);
  });

  return fields;
}, {});

function autofill(e) {
  e.preventDefault();
  billingFields['invittes'].input.value = '100';
  billingFields['starttime'].input.value = 'Jan 19th, 9:00 am';
  billingFields['closetime'].input.value = 'Jan 19th 6:00 pm';
  billingFields['budgets'].input.value = '2000 dollars';
  billingFields['deliverytime'].input.value = 'Jan 19th 12:01 pm';
  billingFields['customization'].input.value = 'None';

  Object.keys(billingFields).forEach(function (field) {
    clearFieldValidations(billingFields[field]);
  });
}

document.getElementById('autofill').addEventListener('click', autofill);

function clearFieldValidations (field) {
  field.help.innerText = '';
  field.help.parentNode.classList.remove('has-error');
}


function validateBillingFields() {
  var isValid = true;

  Object.keys(billingFields).forEach(function (fieldName) {
    var fieldEmpty = false;
    var field = billingFields[fieldName];

    if (field.optional) {
      return;
    }

    fieldEmpty = field.input.value.trim() == '';

    if (fieldEmpty) {
      isValid = false;
      field.help.innerText = 'Field cannot be blank.';
      field.help.parentNode.classList.add('has-error');
    } else {
      clearFieldValidations(field);
    }
  });

  return isValid;
}

function start() {
  getClientToken();
}

function getClientToken() {
  var xhr = new XMLHttpRequest();

  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 201) {
      onFetchClientToken(JSON.parse(xhr.responseText).client_token);
    }
  };
  xhr.open("GET", "https://braintree-sample-merchant.herokuapp.com/client_token", true);

  xhr.send();
}

function setupDropin (clientToken) {
  return braintree.dropin.create({
    authorization: clientToken,
    container: '#drop-in',
    threeDSecure: {
      amount: '100.00'
    }
  })
}

function onFetchClientToken(clientToken) {
  return setupDropin(clientToken).then(function(instance) {
    dropin = instance;

    setupForm();
  }).catch(function (err) {
     console.log('component error:', err);
  });
}

function setupForm() {
  enablePayNow();
}

function enablePayNow() {
  payBtn.removeAttribute('disabled');
}

function showNonce(payload, liabilityShift) {
  nonceSpan.textContent = "Liability shifted: " + liabilityShift;
  nonceInput.value = payload.nonce;
  payGroup.classList.add('hidden');
  payGroup.style.display = 'none';
  nonceGroup.classList.remove('hidden');
}

payBtn.addEventListener('click', function(event) {
  payBtn.setAttribute('disabled', 'disabled');
  payBtn.value = 'Processing...';

  var billingIsValid = validateBillingFields();

  if (!billingIsValid) {
    payBtn.removeAttribute('disabled');

    return;
  }

  dropin.requestPaymentMethod({

    threeDSecure: {
      invittes: billingFields['invittes'].input.value,

      billingAddress: {
        starttime: billingFields['starttime'].input.value,
        closetime: billingFields['closetime'].input.value,
        budgets: billingFields['budgets'].input.value, // remove (), spaces, and - from phone number
        deliverytime: billingFields['deliverytime'].input.value,
        customization: billingFields['customization'].input.value,
      }
    }
  }, function(err, payload) {
    if (err) {
      console.log('tokenization error:');
      console.log(err);
      dropin.clearSelectedPaymentMethod();
      enablePayNow();

      return;
    }

    if (!payload.liabilityShifted) {
      console.log('Liability did not shift', payload);
      showNonce(payload, false);
      return;
    }

    console.log('verification success:', payload);
    showNonce(payload, true);
      // send nonce and verification data to your server
  });
});

start();
