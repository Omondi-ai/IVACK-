"use strict";

// Online status indicator
document.addEventListener('DOMContentLoaded', function () {
  // Update online status periodically
  function updateOnlineStatus() {
    fetch('/accounts/update_online_status/').then(function (response) {
      return response.json();
    }).then(function (data) {
      console.log('Online status updated');
    });
  } // Update every 5 minutes


  setInterval(updateOnlineStatus, 5 * 60 * 1000); // Update on page load

  updateOnlineStatus(); // Mark notifications as read when dropdown is shown

  var notificationDropdown = document.getElementById('notificationDropdown');

  if (notificationDropdown) {
    notificationDropdown.addEventListener('shown.bs.dropdown', function () {
      fetch('/accounts/mark_notifications_read/').then(function (response) {
        return response.json();
      }).then(function (data) {
        var badge = document.querySelector('.notification-badge');

        if (badge) {
          badge.style.display = 'none';
        }
      });
    });
  } // Initialize tooltips


  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
});
document.querySelector('#message-form').addEventListener('submit', function _callee(e) {
  var messageInput, fileInput, formData, response;
  return regeneratorRuntime.async(function _callee$(_context) {
    while (1) {
      switch (_context.prev = _context.next) {
        case 0:
          e.preventDefault();
          messageInput = document.querySelector('#id_text');
          fileInput = document.querySelector('#id_attachment');
          formData = new FormData();
          formData.append('text', messageInput.value);

          if (fileInput.files[0]) {
            formData.append('attachment', fileInput.files[0]);
          }

          formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
          _context.prev = 7;
          _context.next = 10;
          return regeneratorRuntime.awrap(fetch(window.location.href, {
            method: 'POST',
            body: formData
          }));

        case 10:
          response = _context.sent;

          if (response.ok) {
            messageInput.value = '';
            fileInput.value = '';
          }

          _context.next = 17;
          break;

        case 14:
          _context.prev = 14;
          _context.t0 = _context["catch"](7);
          console.error('Error:', _context.t0);

        case 17:
        case "end":
          return _context.stop();
      }
    }
  }, null, null, [[7, 14]]);
});
//# sourceMappingURL=main.dev.js.map
