document.addEventListener("DOMContentLoaded", function () {
    const notesTextarea = document.querySelector('.campaign-notes');
    if (notesTextarea) {
        function adjustHeight() {
            notesTextarea.style.height = 'auto';
            notesTextarea.style.height = notesTextarea.scrollHeight + 'px';
        }

        notesTextarea.addEventListener('input', adjustHeight);
        adjustHeight();
    }

    const searchName = document.getElementById("search-npc-name");
    const filterClass = document.getElementById("filter-npc-class");
    const filterLocation = document.getElementById("filter-npc-location");
    const filterLevel = document.getElementById("filter-npc-level");
    const npcRows = document.querySelectorAll(".npc-row");

    function filterNpcTable() {
        const nameQuery = searchName ? searchName.value.toLowerCase().trim() : "";
        const classQuery = filterClass ? filterClass.value.trim().toLowerCase() : "";
        const locationQuery = filterLocation ? filterLocation.value.trim().toLowerCase() : "";
        const levelQuery = filterLevel ? parseInt(filterLevel.value.trim()) : NaN;

        npcRows.forEach(row => {
            const name = row.dataset.name?.toLowerCase() || "";
            const charClass = row.dataset.class?.toLowerCase() || "";
            const location = row.dataset.location?.toLowerCase() || "";
            const level = parseInt(row.dataset.level) || 0;

            const matchesName = !nameQuery || name.includes(nameQuery);
            const matchesClass = !classQuery || charClass.includes(classQuery);
            const matchesLocation = !locationQuery || location.includes(locationQuery);
            const matchesLevel = isNaN(levelQuery) || level === levelQuery;

            if (matchesName && matchesClass && matchesLocation && matchesLevel) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    }

    if (npcRows.length > 0) {
        [searchName, filterClass, filterLocation, filterLevel].forEach(input => {
            input?.addEventListener("input", filterNpcTable);
        });
    }

    const spellRows = document.querySelectorAll(".spell-row");
    const spellSearchName = document.getElementById("search-spell-name");
    const spellFilterLevel = document.getElementById("filter-spell-level");

    function filterSpellTable() {
        const nameQuery = spellSearchName ? spellSearchName.value.toLowerCase().trim() : "";
        const levelQuery = spellFilterLevel ? parseInt(spellFilterLevel.value.trim()) : "";

        spellRows.forEach(row => {
            const name = row.dataset.name?.toLowerCase() || "";
            const level = parseInt(row.dataset.level) || 0;

            const matchesName = name.includes(nameQuery);
            const matchesLevel = !levelQuery || level === parseInt(levelQuery);

            if (matchesName && matchesLevel) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    }

    if (spellRows.length > 0) {
        [spellSearchName, spellFilterLevel].forEach(input => {
            input?.addEventListener("input", filterSpellTable);
        });
    }

    const itemRows = document.querySelectorAll(".item-row");
    const itemNameInput = document.getElementById("search-item-name");
    const itemTypeInput = document.getElementById("filter-item-type");
    const itemRarityInput = document.getElementById("filter-rarity");

    function filterItemTable() {
        const nameQuery = itemNameInput ? itemNameInput.value.toLowerCase().trim() : "";
        const typeQuery = itemTypeInput ? itemTypeInput.value.trim().toLowerCase() : "";
        const rarityQuery = itemRarityInput ? itemRarityInput.value.trim().toLowerCase() : "";

        itemRows.forEach(row => {
            const name = row.dataset.name?.toLowerCase() || "";
            const type = row.dataset.type?.toLowerCase() || "";
            const rarity = row.dataset.rarity?.toLowerCase() || "";

            const matchesName = !nameQuery || name.includes(nameQuery);
            const matchesType = !typeQuery || type.includes(typeQuery);
            const matchesRarity = !rarityQuery || rarity.includes(rarityQuery);

            if (matchesName && matchesType && matchesRarity) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    }

    if (itemRows.length > 0) {
        [itemNameInput, itemTypeInput, itemRarityInput].forEach(input => {
            input?.addEventListener("input", filterItemTable);
        });
    }

    const monsterRows = document.querySelectorAll(".monster-row");
    const monsterNameInput = document.getElementById("search-monster-name");
    const monsterTypeInput = document.getElementById("filter-monster-type");
    const monsterCrInput = document.getElementById("filter-cr");

    function filterMonsterTable() {
        const nameQuery = monsterNameInput ? monsterNameInput.value.toLowerCase().trim() : "";
        const typeQuery = monsterTypeInput ? monsterTypeInput.value.trim().toLowerCase() : "";
        const crQuery = monsterCrInput ? monsterCrInput.value.trim().toLowerCase() : "";

        monsterRows.forEach(row => {
            const name = row.dataset.name?.toLowerCase() || "";
            const type = row.dataset.type?.toLowerCase() || "";
            const cr = row.dataset.cr?.toLowerCase() || "";

            const matchesName = !nameQuery || name.includes(nameQuery);
            const matchesType = !typeQuery || type.includes(typeQuery);
            const matchesCr = !crQuery || cr.includes(crQuery);

            if (matchesName && matchesType && matchesCr) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    }

    if (monsterRows.length > 0) {
        [monsterNameInput, monsterTypeInput, monsterCrInput].forEach(input => {
            input?.addEventListener("input", filterMonsterTable);
        });
    }

    const locationRows = document.querySelectorAll(".location-row");
    const locationNameInput = document.getElementById("search-location-name");
    const locationTypeInput = document.getElementById("filter-location-type");

    function filterLocationTable() {
        const nameQuery = locationNameInput ? locationNameInput.value.toLowerCase().trim() : "";
        const typeQuery = locationTypeInput ? locationTypeInput.value.trim().toLowerCase() : "";

        locationRows.forEach(row => {
            const name = row.dataset.name?.toLowerCase() || "";
            const type = row.dataset.type?.toLowerCase() || "";

            const matchesName = !nameQuery || name.includes(nameQuery);
            const matchesType = !typeQuery || type.includes(typeQuery);

            if (matchesName && matchesType) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    }

    if (locationRows.length > 0) {
        [locationNameInput, locationTypeInput].forEach(input => {
            input?.addEventListener("input", filterLocationTable);
        });
    }
});