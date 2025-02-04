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