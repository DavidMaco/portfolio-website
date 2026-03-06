/* ================================================================
   DAVID IGBONAJU — PORTFOLIO INTERACTIONS
   Scroll animations, navigation, counter animation, back-to-top.
   ================================================================ */

(function () {
  "use strict";

  /* ── Scroll-Driven Navbar ── */
  const nav = document.querySelector(".nav");
  if (nav) {
    const onScroll = () => nav.classList.toggle("scrolled", window.scrollY > 32);
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ── Mobile Nav Toggle (with hamburger → X animation) ── */
  const toggle = document.querySelector(".nav-toggle");
  const links  = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", () => {
      links.classList.toggle("open");
      toggle.classList.toggle("open");
    });
    links.querySelectorAll("a").forEach(a =>
      a.addEventListener("click", () => {
        links.classList.remove("open");
        toggle.classList.remove("open");
      })
    );
  }

  /* ── Intersection Observer Animations ── */
  const observed = document.querySelectorAll("[data-animate]");
  if (observed.length && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("visible");
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: "0px 0px -40px 0px" }
    );
    observed.forEach((el) => io.observe(el));
  } else {
    observed.forEach((el) => el.classList.add("visible"));
  }

  /* ── Counter Animation ── */
  const counters = document.querySelectorAll("[data-count]");
  if (counters.length && "IntersectionObserver" in window) {
    const counterIO = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (!e.isIntersecting) return;
          const el = e.target;
          const raw = el.getAttribute("data-count");
          const suffix = el.getAttribute("data-suffix") || "";
          const target = parseInt(raw, 10);
          if (isNaN(target)) return;
          counterIO.unobserve(el);

          const duration = 1200;
          const start = performance.now();
          const step = (now) => {
            const progress = Math.min((now - start) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 4); // ease-out quart
            const current = Math.round(eased * target);
            el.textContent = current.toLocaleString() + suffix;
            if (progress < 1) requestAnimationFrame(step);
          };
          requestAnimationFrame(step);
        });
      },
      { threshold: 0.3 }
    );
    counters.forEach((el) => {
      el.textContent = "0";
      counterIO.observe(el);
    });
  }

  /* ── Smooth Scroll for Anchor Links ── */
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener("click", (e) => {
      const id = a.getAttribute("href");
      if (id === "#") return;
      const target = document.querySelector(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });

  /* ── Back to Top Button ── */
  const backBtn = document.querySelector(".back-to-top");
  if (backBtn) {
    const toggleBack = () => backBtn.classList.toggle("visible", window.scrollY > 400);
    window.addEventListener("scroll", toggleBack, { passive: true });
    toggleBack();
    backBtn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* ── Active Nav Section Tracking ── */
  const sections = document.querySelectorAll("section[id]");
  const navLinks = document.querySelectorAll(".nav-links a");
  if (sections.length && navLinks.length && "IntersectionObserver" in window) {
    const sectionIO = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const id = entry.target.getAttribute("id");
            navLinks.forEach((link) => {
              const href = link.getAttribute("href") || "";
              link.classList.toggle("active", href.includes("#" + id));
            });
          }
        });
      },
      { threshold: 0.3, rootMargin: "-80px 0px -40% 0px" }
    );
    sections.forEach((s) => sectionIO.observe(s));
  }
})();
