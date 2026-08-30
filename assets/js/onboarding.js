document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('onboardingForm');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            console.log('Onboarding step 1 submitted.');
            // Proceed to next step...
        });
    }
});
