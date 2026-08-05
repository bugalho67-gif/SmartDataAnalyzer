// Scroll-triggered animations using IntersectionObserver
const revealElements = document.querySelectorAll('.reveal');

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
});

revealElements.forEach(el => revealObserver.observe(el));

// Parallax effect for hero orbs
const heroOrbs = document.querySelectorAll('.hero-orb-1, .hero-orb-2, .hero-orb-3');

window.addEventListener('scroll', () => {
  const scrolled = window.pageYOffset;
  heroOrbs.forEach((orb, index) => {
    const speed = 0.2 + (index * 0.1);
    orb.style.transform = `translateY(${scrolled * speed}px)`;
  });
}, { passive: true });

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});
