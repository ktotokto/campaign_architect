function calculateModifier(value) {
    return Math.floor((value - 10) / 2);
}

function updateModifier(inputId, outputId) {
    const input = document.getElementById(inputId);
    const output = document.getElementById(outputId);

    if (!input || !output) return;

    const value = parseInt(input.value);
    const modifier = isNaN(value) ? 0 : calculateModifier(value);
    output.textContent = modifier >= 0 ? '+' + modifier : modifier;
}

function setupListeners() {
    const stats = ['str', 'dex', 'con', 'int', 'wis', 'cha'];
    stats.forEach(stat => {
        const input = document.getElementById(stat);
        if (input) {
            input.addEventListener('input', () => {
                updateModifier(stat, 'mod-' + stat);
            });
        }
    });
}

window.onload = function () {
    setupListeners();
    ['str', 'dex', 'con', 'int', 'wis', 'cha'].forEach(stat => {
        updateModifier(stat, 'mod-' + stat);
    });
};