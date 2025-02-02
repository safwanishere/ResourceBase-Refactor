const easeOutQuart = (x) => {
    return 1 - Math.pow(1 - x, 4);
};

const animateValue = (element, start, end, duration, options = {}) => {
    const config = {
        prefix: '',
        suffix: '',
        decimal: 0,
        easing: easeOutQuart,
        ...options
    };

    let startTimestamp = null;

    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;

        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const easedProgress = config.easing(progress);

        const currentValue = Math.floor(start + (end - start) * easedProgress);

        const formattedValue = currentValue.toLocaleString();

        element.textContent = `${config.prefix}${formattedValue}${config.suffix}`;

        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };

    window.requestAnimationFrame(step);
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const element = entry.target;
            const target = parseInt(element.getAttribute('data-target'));
            const suffix = element.getAttribute('data-suffix') || '';

            animateValue(element, 0, target, 5000, {
                suffix: suffix
            });

            observer.unobserve(element);
        }
    });
}, { threshold: 0.5 });

document.querySelectorAll('.stat-value').forEach(stat => {
    observer.observe(stat);
});



    document.querySelectorAll('.faq-trigger').forEach(trigger => {
        trigger.addEventListener('click', () => {
            const faqItem = trigger.closest('.faq-item');
            const isOpen = faqItem.getAttribute('data-open') === 'true';

            document.querySelectorAll('.faq-item').forEach(item => {
                item.setAttribute('data-open', 'false');
            });

            faqItem.setAttribute('data-open', !isOpen);
        });
    });

// toggles the side menu when the hamburger icon is clicked
function toggleMenu() {
    // get the side menu element by its ID
    const sideMenu = document.getElementById('sideMenu');
    
    // check if the menu is already visible (right is 0px)
    // if it's visible, slide it out by setting right to -250px
    // if it's hidden, slide it in by setting right to 0px
    const menuRight = sideMenu.style.right === "0px" ? "-250px" : "0px";
    
    // update the right position to either show or hide the menu
    sideMenu.style.right = menuRight;
}

