(function () {
  'use strict';

  var overlay = null;

  function showModal() {
    if (!overlay) {
      overlay = document.getElementById('tc-demo-overlay');
    }
    if (overlay) {
      overlay.classList.add('active');
      overlay.focus();
      document.body.style.overflow = 'hidden';
    }
  }

  function hideModal() {
    if (overlay) {
      overlay.classList.remove('active');
      document.body.style.overflow = '';
    }
    // Redirect to shop
    if (typeof tcModal !== 'undefined' && tcModal.shopUrl) {
      window.location.href = tcModal.shopUrl;
    }
  }

  function init() {
    overlay = document.getElementById('tc-demo-overlay');

    // Close on Keep Exploring button
    var closeBtn = document.getElementById('tc-modal-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', function (e) {
        e.preventDefault();
        hideModal();
      });
    }

    // Close on overlay background click
    if (overlay) {
      overlay.addEventListener('click', function (e) {
        if (e.target === overlay) {
          hideModal();
        }
      });
    }

    // Close on Escape key.
    //
    // Only when the modal is actually open. This listener is on the document
    // and the script loads on every page, so an unguarded version treated
    // Escape anywhere on the site as "close the checkout modal" and ran
    // hideModal(), whose second half redirects to the shop unconditionally.
    // Pressing Escape on the search page therefore threw the visitor off it —
    // and Escape is the standard gesture for dismissing a suggestions
    // dropdown, so the search-as-you-type box made that reachable by accident
    // rather than only by a stray keystroke.
    document.addEventListener('keydown', function (e) {
      if ((e.key === 'Escape' || e.keyCode === 27) && overlay && overlay.classList.contains('active')) {
        hideModal();
      }
    });

    // Intercept checkout form submission
    var checkoutForm = document.querySelector('form.woocommerce-checkout');
    if (checkoutForm) {
      checkoutForm.addEventListener('submit', function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        showModal();
        return false;
      }, true);
    }

    // Intercept Place Order button click
    document.addEventListener('click', function (e) {
      var target = e.target;
      if (
        target &&
        (target.id === 'place_order' ||
          target.classList.contains('place-order') ||
          (target.type === 'submit' &&
            target.closest &&
            target.closest('form.woocommerce-checkout')))
      ) {
        e.preventDefault();
        e.stopImmediatePropagation();
        showModal();
        return false;
      }
    }, true);

    // Show modal on checkout page load (optional: uncomment to show immediately)
    // if (document.body.classList.contains('woocommerce-checkout')) {
    //   showModal();
    // }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
