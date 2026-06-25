// Premium portfolio interactions
const revealItems = document.querySelectorAll(
  '.showcase-card, .project-card, .post-card, .service-card, .focus-card, .content-panel, .skill-cloud span'
);

if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );

  revealItems.forEach((el) => {
    el.classList.add('reveal-item');
    observer.observe(el);
  });
}

const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-item');

window.addEventListener('scroll', () => {
  let current = 'home';
  sections.forEach((sec) => {
    if (window.scrollY >= sec.offsetTop - 160) current = sec.id;
  });
  navLinks.forEach((link) => {
    link.classList.toggle('active', link.getAttribute('href') === `#${current}`);
  });
});
