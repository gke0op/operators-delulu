// main.js — Operators Delulu
(function() {
  'use strict';

  // ─── Fade-in on scroll ───
  function initFadeIn() {
    const elements = document.querySelectorAll('h2, h3, p, li, blockquote, hr, .terrain-item, .start-here, .warning-block, .block');

    const observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.05,
      rootMargin: '0px 0px -30px 0px'
    });

    elements.forEach(function(el) {
      el.classList.add('fade-in');
      observer.observe(el);
    });

    // Show header immediately
    const header = document.querySelector('.page-header');
    if (header) header.classList.add('visible');
  }

  // ─── Active nav highlight ───
  function initNav() {
    const body = document.body;
    const section = body.className.match(/section-(\w+)/);
    if (!section) return;

    const navLinks = document.querySelectorAll('.topnav .nav-links a');
    navLinks.forEach(function(link) {
      const href = link.getAttribute('href');
      if (href && href.includes(section[1])) {
        link.classList.add('active');
      }
    });
  }

  // ─── Breathing circle (for index page) ───
  function initBreathingCircle() {
    const circle = document.querySelector('.breathing-circle');
    if (!circle) return;

    // Sync with vagus rhythm: 4s inhale, 7s hold, 8s exhale = 19s cycle
    circle.style.animationDuration = '19s';
    circle.style.animationTimingFunction = 'ease-in-out';
  }

  // ─── Gateway section: subtle text reveal ───
  function initGatewayReveal() {
    if (!document.body.classList.contains('section-gateway')) return;

    // Slightly darker background for gateway
    document.documentElement.style.setProperty('--bg', '#030303');

    // Add a subtle pulsing glow to the page header
    const header = document.querySelector('.page-header h1');
    if (header) {
      header.style.textShadow = '0 0 30px rgba(114, 9, 183, 0.3)';
    }
  }

  // ─── Keyboard navigation ───
  function initKeyboardNav() {
    document.addEventListener('keydown', function(e) {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

      if (e.key === 'ArrowRight' || e.key === 'j') {
        const next = document.querySelector('.page-nav .next a');
        if (next) next.click();
      }
      if (e.key === 'ArrowLeft' || e.key === 'k') {
        const prev = document.querySelector('.page-nav .prev a');
        if (prev) prev.click();
      }
    });
  }

  // ─── Init ───
  document.addEventListener('DOMContentLoaded', function() {
    initFadeIn();
    initNav();
    initBreathingCircle();
    initGatewayReveal();
    initKeyboardNav();
  });
})();
