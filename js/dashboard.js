// Interactive Dashboard
class Dashboard {
  constructor() {
    this.currentTab = 'overview';
    this.tabs = document.querySelectorAll('.dashboard-tab');
    this.charts = {};
    this.init();
  }
  
  init() {
    this.tabs.forEach(tab => {
      tab.addEventListener('click', () => this.switchTab(tab.dataset.tab));
    });
    
    this.initLineChart();
    this.initHeatmap();
    this.animateMetrics();
  }
  
  switchTab(tabName) {
    this.currentTab = tabName;
    this.tabs.forEach(t => t.classList.toggle('active', t.dataset.tab === tabName));
    
    // Simulate tab content change with fade
    const body = document.querySelector('.dashboard-body');
    body.style.opacity = '0.5';
    setTimeout(() => {
      body.style.opacity = '1';
      this.updateChartData();
    }, 200);
  }
  
  initLineChart() {
    const canvas = document.getElementById('mainChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);
    
    this.drawLineChart(ctx, rect.width, rect.height);
  }
  
  drawLineChart(ctx, width, height) {
    const padding = 40;
    const chartWidth = width - padding * 2;
    const chartHeight = height - padding * 2;
    
    // Clear
    ctx.clearRect(0, 0, width, height);
    
    // Data points
    const points = [30, 45, 35, 55, 48, 62, 58, 75, 68, 82, 78, 90];
    const maxVal = 100;
    
    // Draw grid lines
    ctx.strokeStyle = 'rgba(255,255,255,0.05)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      const y = padding + (chartHeight / 4) * i;
      ctx.beginPath();
      ctx.moveTo(padding, y);
      ctx.lineTo(width - padding, y);
      ctx.stroke();
    }
    
    // Draw area
    ctx.beginPath();
    ctx.moveTo(padding, padding + chartHeight);
    
    points.forEach((val, i) => {
      const x = padding + (chartWidth / (points.length - 1)) * i;
      const y = padding + chartHeight - (val / maxVal) * chartHeight;
      if (i === 0) ctx.lineTo(x, y);
      else {
        const prevX = padding + (chartWidth / (points.length - 1)) * (i - 1);
        const prevY = padding + chartHeight - (points[i-1] / maxVal) * chartHeight;
        const cpX = (prevX + x) / 2;
        ctx.bezierCurveTo(cpX, prevY, cpX, y, x, y);
      }
    });
    
    ctx.lineTo(width - padding, padding + chartHeight);
    ctx.closePath();
    
    const gradient = ctx.createLinearGradient(0, padding, 0, height - padding);
    gradient.addColorStop(0, 'rgba(59, 130, 246, 0.2)');
    gradient.addColorStop(1, 'rgba(59, 130, 246, 0)');
    ctx.fillStyle = gradient;
    ctx.fill();
    
    // Draw line
    ctx.beginPath();
    points.forEach((val, i) => {
      const x = padding + (chartWidth / (points.length - 1)) * i;
      const y = padding + chartHeight - (val / maxVal) * chartHeight;
      if (i === 0) ctx.moveTo(x, y);
      else {
        const prevX = padding + (chartWidth / (points.length - 1)) * (i - 1);
        const prevY = padding + chartHeight - (points[i-1] / maxVal) * chartHeight;
        const cpX = (prevX + x) / 2;
        ctx.bezierCurveTo(cpX, prevY, cpX, y, x, y);
      }
    });
    
    ctx.strokeStyle = '#3b82f6';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    // Draw points
    points.forEach((val, i) => {
      const x = padding + (chartWidth / (points.length - 1)) * i;
      const y = padding + chartHeight - (val / maxVal) * chartHeight;
      
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.fillStyle = '#0a0a0a';
      ctx.fill();
      ctx.strokeStyle = '#3b82f6';
      ctx.lineWidth = 2;
      ctx.stroke();
    });
  }
  
  initHeatmap() {
    const cells = document.querySelectorAll('.heatmap-cell');
    cells.forEach(cell => {
      const value = parseFloat(cell.dataset.value);
      const intensity = Math.abs(value);
      const isPositive = value >= 0;
      
      const r = isPositive ? Math.floor(34 * intensity) : Math.floor(239 * intensity);
      const g = isPositive ? Math.floor(197 * intensity) : Math.floor(68 * intensity);
      const b = isPositive ? Math.floor(94 * intensity) : Math.floor(68 * intensity);
      
      cell.style.backgroundColor = `rgba(${r}, ${g}, ${b}, ${0.1 + intensity * 0.3})`;
      cell.style.color = isPositive ? '#22c55e' : '#ef4444';
    });
  }
  
  animateMetrics() {
    const metrics = document.querySelectorAll('.metric-value[data-target]');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.dataset.target);
          const suffix = el.dataset.suffix || '';
          let current = 0;
          const increment = target / 60;
          const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
              current = target;
              clearInterval(timer);
            }
            el.textContent = Math.floor(current).toLocaleString() + suffix;
          }, 30);
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.5 });
    
    metrics.forEach(m => observer.observe(m));
  }
  
  updateChartData() {
    const canvas = document.getElementById('mainChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const rect = canvas.getBoundingClientRect();
    this.drawLineChart(ctx, rect.width, rect.height);
  }
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  if (document.querySelector('.dashboard-container')) {
    new Dashboard();
  }
});

// Handle resize for charts
window.addEventListener('resize', () => {
  const dashboard = document.querySelector('.dashboard-container');
  if (dashboard) {
    const canvas = document.getElementById('mainChart');
    if (canvas) {
      const ctx = canvas.getContext('2d');
      const rect = canvas.parentElement.getBoundingClientRect();
      canvas.width = rect.width * window.devicePixelRatio;
      canvas.height = rect.height * window.devicePixelRatio;
      ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
      // Redraw would need the Dashboard instance
    }
  }
});
