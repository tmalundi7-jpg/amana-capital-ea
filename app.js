document.addEventListener('DOMContentLoaded', function() {
  var toggle = document.getElementById('mobile-toggle');
  var nav = document.getElementById('nav-links');
  if (toggle && nav) {
    toggle.addEventListener('click', function() {
      nav.classList.toggle('active');
    });
  }
});
