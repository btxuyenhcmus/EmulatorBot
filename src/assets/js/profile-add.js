/**
 * Access multilogin account
 */

'use strict';

(function () {
  const formAdd = document.getElementById('MultiloginAddForm');

  const fv = FormValidation.formValidation(formAdd, {
    fields: {
      email: {
        validators: {
          notEmpty: {
            message: "Please enter email"
          }
        }
      },
      password: {
        validators: {
          notEmpty: {
            message: "Please enter password"
          }
        }
      }
    },
    plugins: {
      trigger: new FormValidation.plugins.Trigger(),
      bootstrap5: new FormValidation.plugins.Bootstrap5({
        eleValidClass: '',
        rowSelector: '.form-floating'
      }),
      submitButton: new FormValidation.plugins.SubmitButton(),
      autoFocus: new FormValidation.plugins.AutoFocus()
    },
    init: instance => {
      instance.on('plugins.message.placed', function (e) {
        if (e.element.parentElement.classList.contains('input-group')) {
          e.element.parentElement.insertAdjacentElement('afterend', e.messageElement);
        }
      });
    }
  }).on('core.form.valid', function () {
    $('#loading-overlay').show();
    $('#loading-indicator').show();
    var formData = $(formAdd).serialize();
    $.ajax({
      url: formAdd.getAttribute('post'),
      method: 'POST',
      data: formData,
      success: function (response) {
        window.location.href = formAdd.getAttribute('redirect');
      },
      error: function (error) {
        console.log(response);
      },
      complete: function () {
        $('#loading-indicator').hide();
        $('#loading-overlay').hide();
      }
    })
  });
})();