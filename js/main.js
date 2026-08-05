// Main initialization
document.addEventListener('DOMContentLoaded', () => {
  // Initialize all modules
  console.log('SmartDataAnalyzer Landing initialized');
  
  // Add loaded class to body for initial animations
  document.body.classList.add('loaded');
  
  // Preview bar animations in hero
  const previewBars = document.querySelectorAll('.preview-bar');
  previewBars.forEach((bar, i) => {
    const height = 20 + Math.random() * 80;
    setTimeout(() => {
      bar.style.height = height + '%';
    }, 1000 + i * 100);
  });
});
