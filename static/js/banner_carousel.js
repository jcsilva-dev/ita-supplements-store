
  (function () {
    const carousel = document.getElementById("bannerCarousel");
    if (!carousel) return;

    const track = document.getElementById("bannerTrack");
    if (!track) return;

    const slides = Array.from(track.querySelectorAll(".banner-carousel__slide"));

    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");

    const dotsContainer = document.getElementById("bannerDots");

    let currentIndex = 0;

    const AUTOPLAY_DELAY = 4500;
    let autoplayTimer = null;

    const dots = slides.map((_, index) => {
      const dot = document.createElement("button");
      dot.classList.add("banner-carousel__dot");
      dot.setAttribute("type", "button");
      dot.setAttribute("aria-label", `Ir para banner ${index + 1}`);

      dot.addEventListener("click", () => {
        goToSlide(index);
        restartAutoplay();
      });

      dotsContainer.appendChild(dot);
      return dot;
    });

    function goToSlide(index) {
      if (slides.length === 0) return;

      if (index < 0) index = slides.length - 1;
      if (index >= slides.length) index = 0;

      currentIndex = index;

      track.style.transform = `translateX(-${currentIndex * 100}%)`;

      dots.forEach(d => d.classList.remove("is-active"));
      if (dots[currentIndex]) dots[currentIndex].classList.add("is-active");
    }

    if (prevBtn) {
      prevBtn.addEventListener("click", () => {
        goToSlide(currentIndex - 1);
        restartAutoplay();
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", () => {
        goToSlide(currentIndex + 1);
        restartAutoplay();
      });
    }

    function startAutoplay() {
      if (slides.length <= 1) return;

      autoplayTimer = setInterval(() => {
        goToSlide(currentIndex + 1);
      }, AUTOPLAY_DELAY);
    }

    function stopAutoplay() {
      if (autoplayTimer) clearInterval(autoplayTimer);
      autoplayTimer = null;
    }

    function restartAutoplay() {
      stopAutoplay();
      startAutoplay();
    }

    carousel.addEventListener("mouseenter", stopAutoplay);
    carousel.addEventListener("mouseleave", startAutoplay);

    let startX = 0;
    let endX = 0;
    let isDragging = false;

    carousel.addEventListener("touchstart", (e) => {
      startX = e.touches[0].clientX;
      isDragging = true;
      stopAutoplay();
    }, { passive: true });

    carousel.addEventListener("touchmove", (e) => {
      if (!isDragging) return;
      endX = e.touches[0].clientX;
    }, { passive: true });

    carousel.addEventListener("touchend", () => {
      if (!isDragging) return;
      isDragging = false;

      const diff = startX - endX;

      if (diff > 45) {
        goToSlide(currentIndex + 1);
      } else if (diff < -45) {
        goToSlide(currentIndex - 1);
      }

      startAutoplay();
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "ArrowLeft") {
        goToSlide(currentIndex - 1);
        restartAutoplay();
      }

      if (e.key === "ArrowRight") {
        goToSlide(currentIndex + 1);
        restartAutoplay();
      }
    });

    goToSlide(0);
    startAutoplay();

    if (slides.length <= 1) {
      if (prevBtn) prevBtn.style.display = "none";
      if (nextBtn) nextBtn.style.display = "none";
      if (dotsContainer) dotsContainer.style.display = "none";
    }
  })();