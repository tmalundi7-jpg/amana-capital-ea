document.addEventListener('DOMContentLoaded', function() {
  var toggle = document.getElementById('mobile-toggle');
  var nav = document.getElementById('nav-links');
  if (toggle && nav) {
    toggle.innerHTML = '<span class="mobile-toggle-bar"></span><span class="mobile-toggle-bar"></span><span class="mobile-toggle-bar"></span>';
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open menu');
    var navbar = toggle.closest('.navbar') || document.querySelector('.navbar');

    function openMenu() {
      nav.classList.add('active');
      if (navbar) navbar.classList.add('nav-open');
      toggle.classList.add('active');
      toggle.setAttribute('aria-expanded', 'true');
      toggle.setAttribute('aria-label', 'Close menu');
      document.body.classList.add('nav-open');
    }

    function closeMenu() {
      nav.classList.remove('active');
      if (navbar) navbar.classList.remove('nav-open');
      toggle.classList.remove('active');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Open menu');
      document.body.classList.remove('nav-open');
    }

    toggle.addEventListener('click', function(e) {
      if (e) e.stopPropagation();
      var isOpen = nav.classList.contains('active') || (navbar && navbar.classList.contains('nav-open'));
      if (isOpen) { closeMenu(); } else { openMenu(); }
    });

    var navLinks = nav.querySelectorAll('a');
    navLinks.forEach(function(link) {
      link.addEventListener('click', closeMenu);
    });

    document.addEventListener('click', function(e) {
      var isOpen = nav.classList.contains('active') || (navbar && navbar.classList.contains('nav-open'));
      if (!isOpen) return;
      if (!toggle.contains(e.target) && !nav.contains(e.target)) {
        closeMenu();
      }
    });

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') closeMenu();
    });

    window.addEventListener('resize', function() {
      if (window.innerWidth > 1150) closeMenu();
    });
  }
});
