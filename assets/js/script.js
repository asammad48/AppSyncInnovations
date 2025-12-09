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
  const scrollToTopBtn = document.getElementById('scrollToTop');
  
  if (header) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 100) {
        header.classList.add('scrolled');
        if (scrollToTopBtn) scrollToTopBtn.classList.add('visible');
      } else {
        header.classList.remove('scrolled');
        if (scrollToTopBtn) scrollToTopBtn.classList.remove('visible');
      }
    });
  }

  if (scrollToTopBtn) {
    scrollToTopBtn.addEventListener('click', function() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
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

  document.querySelectorAll('.service-card, .feature-item, .testimonial-card, .pricing-card, .blog-card').forEach((el, index) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = `all 0.6s cubic-bezier(0.4, 0, 0.2, 1) ${index * 0.1}s`;
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
    const numbers = document.querySelectorAll('.number, .hero-stat-number');
    numbers.forEach(num => {
      const target = parseInt(num.getAttribute('data-target')) || parseInt(num.textContent);
      if (!target) return;
      
      const duration = 2000;
      const step = target / (duration / 16);
      let current = 0;
      let hasAnimated = false;
      
      const updateNumber = () => {
        current += step;
        if (current < target) {
          num.textContent = Math.floor(current) + (num.classList.contains('hero-stat-number') ? '' : '+');
          requestAnimationFrame(updateNumber);
        } else {
          num.textContent = target + (num.classList.contains('hero-stat-number') ? '' : '+');
        }
      };
      
      const numObserver = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting && !hasAnimated) {
          hasAnimated = true;
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
      const href = this.getAttribute('href');
      if (href === '#') return;
      
      e.preventDefault();
      const target = document.querySelector(href);
      if (target) {
        const headerOffset = 80;
        const elementPosition = target.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });
      }
    });
  });

  const langDropdown = document.querySelector('.lang-dropdown');
  const langCurrentBtn = document.getElementById('langCurrentBtn');
  const langOptions = document.getElementById('langOptions');
  
  if (langDropdown && langCurrentBtn && langOptions) {
    langCurrentBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      langDropdown.classList.toggle('open');
    });
    
    document.addEventListener('click', function(e) {
      if (!langDropdown.contains(e.target)) {
        langDropdown.classList.remove('open');
      }
    });
    
    const langOptionItems = langOptions.querySelectorAll('li');
    langOptionItems.forEach(item => {
      item.addEventListener('click', function() {
        const lang = this.dataset.lang;
        const url = this.dataset.url;
        const flag = this.querySelector('.lang-flag').textContent;
        
        langOptionItems.forEach(li => li.classList.remove('active'));
        this.classList.add('active');
        
        langCurrentBtn.querySelector('.lang-flag').textContent = flag;
        langCurrentBtn.querySelector('.lang-name').textContent = lang.toUpperCase();
        
        langDropdown.classList.remove('open');
        
        const currentPath = window.location.pathname;
        const pathParts = currentPath.split('/').filter(p => p);
        const langs = ['es', 'fr', 'pt', 'ca', 'ar', 'ur'];
        
        if (langs.includes(pathParts[0])) {
          pathParts.shift();
        }
        
        let newPath;
        if (lang === 'en') {
          newPath = '/' + pathParts.join('/');
        } else {
          newPath = '/' + lang + '/' + pathParts.join('/');
        }
        
        if (newPath === '/') newPath = '/';
        else if (!newPath.endsWith('/')) newPath += '/';
        
        window.location.href = newPath;
      });
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

  const magneticButtons = document.querySelectorAll('.magnetic-button');
  magneticButtons.forEach(btn => {
    btn.addEventListener('mousemove', function(e) {
      const rect = this.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      
      this.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
    });
    
    btn.addEventListener('mouseleave', function() {
      this.style.transform = 'translate(0, 0)';
    });
  });

  const tiltElements = document.querySelectorAll('.tilt-effect');
  tiltElements.forEach(el => {
    el.addEventListener('mousemove', function(e) {
      const rect = this.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width;
      const y = (e.clientY - rect.top) / rect.height;
      
      const tiltX = (y - 0.5) * 10;
      const tiltY = (x - 0.5) * -10;
      
      this.style.transform = `perspective(1000px) rotateX(${tiltX}deg) rotateY(${tiltY}deg)`;
    });
    
    el.addEventListener('mouseleave', function() {
      this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
    });
  });

  const parallaxShapes = document.querySelectorAll('.parallax-shape');
  window.addEventListener('mousemove', function(e) {
    const x = e.clientX / window.innerWidth;
    const y = e.clientY / window.innerHeight;
    
    parallaxShapes.forEach((shape, index) => {
      const speed = (index + 1) * 20;
      const xOffset = (x - 0.5) * speed;
      const yOffset = (y - 0.5) * speed;
      
      shape.style.transform = `translate(${xOffset}px, ${yOffset}px)`;
    });
  });

  const heroCard = document.querySelector('.hero-card');
  if (heroCard) {
    const bars = heroCard.querySelectorAll('.hero-card-line-bar-fill');
    
    const heroObserver = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) {
        bars.forEach((bar, index) => {
          const width = bar.style.width;
          bar.style.width = '0';
          setTimeout(() => {
            bar.style.transition = 'width 1.5s cubic-bezier(0.4, 0, 0.2, 1)';
            bar.style.width = width;
          }, index * 200);
        });
        heroObserver.unobserve(heroCard);
      }
    });
    
    heroObserver.observe(heroCard);
  }

  const serviceCards = document.querySelectorAll('.service-card');
  serviceCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.boxShadow = '0 25px 50px -12px rgba(50, 32, 99, 0.25)';
    });
    
    card.addEventListener('mouseleave', function() {
      this.style.boxShadow = '';
    });
  });

  const createRipple = (e) => {
    const button = e.currentTarget;
    const ripple = document.createElement('span');
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;
    
    ripple.style.cssText = `
      position: absolute;
      width: ${size}px;
      height: ${size}px;
      left: ${x}px;
      top: ${y}px;
      background: rgba(255, 255, 255, 0.3);
      border-radius: 50%;
      transform: scale(0);
      animation: ripple 0.6s ease-out;
      pointer-events: none;
    `;
    
    button.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
  };

  const rippleStyle = document.createElement('style');
  rippleStyle.textContent = `
    @keyframes ripple {
      to {
        transform: scale(4);
        opacity: 0;
      }
    }
    .btn {
      position: relative;
      overflow: hidden;
    }
  `;
  document.head.appendChild(rippleStyle);

  document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', createRipple);
  });

  const testimonialCards = document.querySelectorAll('.testimonial-card');
  testimonialCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      testimonialCards.forEach(c => {
        if (c !== card) {
          c.style.opacity = '0.7';
          c.style.transform = 'scale(0.98)';
        }
      });
    });
    
    card.addEventListener('mouseleave', function() {
      testimonialCards.forEach(c => {
        c.style.opacity = '1';
        c.style.transform = '';
      });
    });
  });

  const navLinksItems = document.querySelectorAll('.nav-links > li > a:not(.btn)');
  navLinksItems.forEach(link => {
    link.addEventListener('mouseenter', function() {
      this.style.color = '#322063';
    });
    
    link.addEventListener('mouseleave', function() {
      if (!this.classList.contains('active')) {
        this.style.color = '';
      }
    });
  });

  window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const heroSection = document.querySelector('.hero');
    
    if (heroSection) {
      const heroText = heroSection.querySelector('.hero-text');
      const heroImage = heroSection.querySelector('.hero-image');
      
      if (heroText && scrolled < window.innerHeight) {
        heroText.style.transform = `translateY(${scrolled * 0.1}px)`;
        heroText.style.opacity = 1 - (scrolled / window.innerHeight) * 0.5;
      }
      
      if (heroImage && scrolled < window.innerHeight) {
        heroImage.style.transform = `translateY(${scrolled * 0.15}px)`;
      }
    }
  });
});
