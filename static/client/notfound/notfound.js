function follow(pupil, rect, mx, my) {
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;

    const dx = mx - cx;
    const dy = my - cy;

    const angle = Math.atan2(dy, dx);
    const limit = 22;

    pupil.style.transform = `translate(${Math.cos(angle) * limit}px, ${
        Math.sin(angle) * limit
    }px)`;
    }

    const Lp = document.getElementById('pupil-left');
    const Rp = document.getElementById('pupil-right');

    window.addEventListener('mousemove', (e) => {
    follow(
        Lp,
        Lp.parentElement.getBoundingClientRect(),
        e.clientX,
        e.clientY
    );
    follow(
        Rp,
        Rp.parentElement.getBoundingClientRect(),
        e.clientX,
        e.clientY
    );
    });

    /* Auto blink */
    const Llid = document.getElementById('lid-left');
    const Rlid = document.getElementById('lid-right');

    function blink() {
        Llid.classList.add('blink');
        Rlid.classList.add('blink');

        setTimeout(() => {
            Llid.classList.remove('blink');
            Rlid.classList.remove('blink');
        }, 180);

        setTimeout(blink, 2500 + Math.random() * 3000);
    }

    setTimeout(blink, 2000);