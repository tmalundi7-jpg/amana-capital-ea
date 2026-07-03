document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    document.documentElement.setAttribute('data-theme', currentTheme);
    if (toggleBtn) {
        toggleBtn.innerHTML = currentTheme === 'dark' ? '☀️' : '🌙';
    }

    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            const newTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            toggleBtn.innerHTML = newTheme === 'dark' ? '☀️' : '🌙';
        });
    }
});
