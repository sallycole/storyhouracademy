// GoatCounter Analytics
(function() {
    var script = document.createElement('script');
    script.async = true;
    script.src = '//gc.zgo.at/count.js';
    script.setAttribute('data-goatcounter', 'https://storyhour.goatcounter.com/count');
    document.head.appendChild(script);
})();

// Load header and footer
fetch('includes/header.html')
    .then(res => res.text())
    .then(data => {
        document.getElementById('header').innerHTML = data;
        // Initialize header functionality after content is loaded
        initializeHeader();
    });

fetch('includes/footer.html')
    .then(res => res.text())
    .then(data => {
        document.getElementById('footer').innerHTML = data;
    });

function initializeHeader() {
    const dropdowns = document.querySelectorAll('.dropdown');
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    // Mobile menu toggle
    menuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
        menuToggle.setAttribute('aria-expanded', !isExpanded);
        
        // Prevent body scroll when menu is open
        document.body.style.overflow = !isExpanded ? 'hidden' : '';
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.header-content') && navLinks.classList.contains('active')) {
            navLinks.classList.remove('active');
            menuToggle.setAttribute('aria-expanded', 'false');
            document.body.style.overflow = '';
        }
    });
    
    // Handle dropdowns for both desktop and mobile
    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        const content = dropdown.querySelector('.dropdown-content');
        
        toggle.setAttribute('aria-expanded', 'false');
        
        toggle.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation(); // Prevent event from bubbling up
            
            const isExpanded = toggle.getAttribute('aria-expanded') === 'true';
            toggle.setAttribute('aria-expanded', !isExpanded);
            dropdown.classList.toggle('active');
            
            // Close other dropdowns
            dropdowns.forEach(otherDropdown => {
                if (otherDropdown !== dropdown) {
                    otherDropdown.classList.remove('active');
                    otherDropdown.querySelector('.dropdown-toggle').setAttribute('aria-expanded', 'false');
                }
            });
        });

        content.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                toggle.setAttribute('aria-expanded', 'false');
                dropdown.classList.remove('active');
                toggle.focus();
            }
        });
    });
}
