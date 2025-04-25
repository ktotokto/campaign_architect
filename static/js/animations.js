document.addEventListener('DOMContentLoaded', function() {
    const candlesContainer = document.getElementById('candles-container');
    for (let i = 0; i < 8; i++) {
        const candle = document.createElement('div');
        candle.className = 'candle-light';
        candle.style.animationDelay = `${Math.random() * 2}s`;
        candlesContainer.appendChild(candle);
    }

    const dustContainer = document.getElementById('magic-dust-container');
    const particleTypes = ['type1', 'type2', 'type3'];
});