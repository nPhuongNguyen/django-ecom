class MyLoading {
    static show(options = {}) {
        if (document.getElementById('my-loading-overlay')) return;

        const overlay = document.createElement('div');
        overlay.id = 'my-loading-overlay';
        overlay.style.position = 'fixed';
        overlay.style.top = '0';
        overlay.style.left = '0';
        overlay.style.width = '100%';
        overlay.style.height = '100%';
        overlay.style.background = options.background || 'rgba(0,0,0,0.3)';
        overlay.style.display = 'flex';
        overlay.style.alignItems = 'center';
        overlay.style.justifyContent = 'center';
        overlay.style.zIndex = 99999;

        const target = document.createElement('div');
        overlay.appendChild(target);
        document.body.appendChild(overlay);

        const spinner = new Spinner({
            lines: options.lines || 12,
            length: options.length || 8,
            width: options.width || 4,
            radius: options.radius || 10,
            color: options.color || '#3085d6',
            speed: options.speed || 1,
            trail: options.trail || 60
        }).spin(target);

        overlay._spinner = spinner;
    }

    static close() {
        const overlay = document.getElementById('my-loading-overlay');
        if (overlay) {
            if (overlay._spinner) overlay._spinner.stop();
            overlay.remove();
        }
    }
}