document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('newsletterForm');
  if (form) form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = document.getElementById('newsletterMessage');
    message.hidden = false; message.className = 'newsletter-message success'; message.textContent = '✅ Subscribed!';
    form.reset();
  });
});