document.addEventListener('DOMContentLoaded', function() {
  const loader = document.querySelector('.loader-wrapper');
  if (loader) {
    setTimeout(() => {
      loader.classList.add('hidden');
    }, 800);
  }

  const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
  const navLinks = document.querySelector('.nav-links');
  
  if (mobileMenuBtn && navLinks) {
    mobileMenuBtn.addEventListener('click', function() {
      navLinks.classList.toggle('active');
      this.classList.toggle('active');
    });
  }

  const header = document.querySelector('header');
  if (header) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 100) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    });
  }

  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    if (question) {
      question.addEventListener('click', function() {
        const isActive = item.classList.contains('active');
        faqItems.forEach(i => i.classList.remove('active'));
        if (!isActive) {
          item.classList.add('active');
        }
      });
    }
  });

  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.service-card, .feature-item, .testimonial-card, .pricing-card, .blog-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'all 0.6s ease';
    observer.observe(el);
  });

  const style = document.createElement('style');
  style.textContent = `
    .animate-in {
      opacity: 1 !important;
      transform: translateY(0) !important;
    }
  `;
  document.head.appendChild(style);

  const animateNumbers = () => {
    const numbers = document.querySelectorAll('.number');
    numbers.forEach(num => {
      const target = parseInt(num.getAttribute('data-target')) || parseInt(num.textContent);
      const duration = 2000;
      const step = target / (duration / 16);
      let current = 0;
      
      const updateNumber = () => {
        current += step;
        if (current < target) {
          num.textContent = Math.floor(current) + '+';
          requestAnimationFrame(updateNumber);
        } else {
          num.textContent = target + '+';
        }
      };
      
      const numObserver = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting) {
          updateNumber();
          numObserver.unobserve(num);
        }
      });
      
      numObserver.observe(num);
    });
  };
  
  animateNumbers();

  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
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

  const langSwitcher = document.getElementById('langSwitcher');
  if (langSwitcher) {
    langSwitcher.addEventListener('change', function() {
      const lang = this.value;
      const currentPath = window.location.pathname;
      let newPath;
      
      const pathParts = currentPath.split('/').filter(p => p);
      const langs = ['es', 'fr', 'pt', 'ca', 'ar', 'ur'];
      
      if (langs.includes(pathParts[0])) {
        pathParts.shift();
      }
      
      if (lang === 'en') {
        newPath = '/' + pathParts.join('/');
      } else {
        newPath = '/' + lang + '/' + pathParts.join('/');
      }
      
      if (newPath === '/') newPath = '/';
      else if (!newPath.endsWith('/')) newPath += '/';
      
      window.location.href = newPath;
    });
  }

  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      const submitBtn = form.querySelector('button[type="submit"]');
      const originalText = submitBtn.textContent;
      submitBtn.textContent = 'Sending...';
      submitBtn.disabled = true;
      
      setTimeout(() => {
        submitBtn.textContent = 'Sent!';
        setTimeout(() => {
          submitBtn.textContent = originalText;
          submitBtn.disabled = false;
          form.reset();
        }, 2000);
      }, 1500);
    });
  });
});
