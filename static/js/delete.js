document.addEventListener("DOMContentLoaded", function () {
    const playerDeleteButtons = document.querySelectorAll(".delete-btn[data-player-id]");
    const playersList = document.querySelector(".players-list");
    let campaignTitleFromPlayers = "";
    if (playersList) {
        campaignTitleFromPlayers = playersList.dataset?.campaignTitle || "";
    }
    if (!campaignTitleFromPlayers && playerDeleteButtons.length > 0) {
        console.error("Название кампании не найдено для удаления игроков");
        alert("Ошибка: кампания не загружена корректно (игроки)");
    }
    playerDeleteButtons.forEach(button => {
        button.addEventListener("click", async (event) => {
            const playerId = event.target.dataset.playerId;
            if (!playerId) {
                alert("ID игрока не определено");
                return;
            }
            if (!confirm(`Вы уверены, что хотите удалить игрока "${playerId}"?`)) return;
            try {
                const response = await fetch(`/campaigns/${campaignTitleFromPlayers}/delete_player/${playerId}`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" }
                });
                const result = await response.json();
                if (result.success) {
                    const card = event.target.closest(".player-card");
                    if (card) card.remove();
                    alert("Игрок успешно удален");
                } else {
                    alert(result.message || "Ошибка при удалении игрока");
                }
            } catch (error) {
                console.error("Ошибка:", error);
                alert("Произошла ошибка при удалении");
            }
        });
    });

    const npcDeleteButtons = document.querySelectorAll(".npc-delete-btn[data-npc-id]");
    const npcContainer = document.getElementById("npc-container");
    let campaignTitleFromNpcs = "";
    if (npcContainer) {
        campaignTitleFromNpcs = npcContainer.dataset?.campaignTitle || "";
    }
    if (!campaignTitleFromNpcs && npcDeleteButtons.length > 0) {
        console.warn("Контейнер с data-campaign-title не найден для NPC");
        return;
    }
    npcDeleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            const npcId = this.dataset.npcId || this.getAttribute("data-npc-id");
            if (!campaignTitleFromNpcs) {
                alert("Не удалось получить название кампании");
                return;
            }
            if (!confirm("Вы уверены, что хотите удалить этого NPC?")) return;
            fetch(`/campaigns/${encodeURIComponent(campaignTitleFromNpcs)}/delete_npc/${npcId}`, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => {
                if (!response.ok) throw new Error("Ошибка сети при удалении NPC");
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    const row = this.closest("tr") || this.closest(".npc-card");
                    if (row) row.remove();
                    alert("NPC удален");
                } else {
                    alert("Ошибка: " + (data.message || "Не удалось удалить NPC"));
                }
            })
            .catch(err => {
                console.error("Ошибка запроса на удаление NPC:", err);
                alert("Произошла ошибка при удалении NPC");
            });
        });
    });

    const spellDeleteButtons = document.querySelectorAll(".spell-delete-btn[data-spell-id]");
    const spellContainer = document.getElementById("spells-container");
    let campaignTitleFromSpells = "";
    if (spellContainer) {
        campaignTitleFromSpells = spellContainer.dataset?.campaignTitle || "";
    }
    if (!campaignTitleFromSpells && spellDeleteButtons.length > 0) {
        console.warn("Контейнер заклинаний не найден");
        return;
    }
    spellDeleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            const spellId = this.dataset.spellId || this.getAttribute("data-spell-id");
            if (!campaignTitleFromSpells) {
                alert("Не удалось получить название кампании");
                return;
            }
            if (!confirm("Вы уверены, что хотите удалить это заклинание?")) return;
            fetch(`/campaigns/${encodeURIComponent(campaignTitleFromSpells)}/delete_spell/${spellId}`, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => {
                if (!response.ok) throw new Error("Ошибка сети при удалении заклинания");
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    const row = this.closest("tr") || this.closest(".spell-card");
                    if (row) row.remove();
                    alert("Заклинание удалено");
                } else {
                    alert("Ошибка: " + (data.message || "Не удалось удалить заклинание"));
                }
            })
            .catch(err => {
                console.error("Ошибка запроса на удаление заклинания:", err);
                alert("Произошла ошибка при удалении заклинания");
            });
        });
    });

    const itemDeleteButtons = document.querySelectorAll(".item-delete-btn[data-item-id]");
    const itemContainer = document.getElementById("items-container");
    let campaignTitleFromItems = "";
    if (itemContainer) {
        campaignTitleFromItems = itemContainer.dataset?.campaignTitle || "";
    }
    if (!campaignTitleFromItems && itemDeleteButtons.length > 0) {
        console.warn("Контейнер с data-campaign-title не найден для предметов");
        return;
    }
    itemDeleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            const itemId = this.dataset.itemId || this.getAttribute("data-item-id");
            if (!campaignTitleFromItems) {
                alert("Не удалось получить название кампании");
                return;
            }
            if (!confirm("Вы уверены, что хотите удалить этот предмет?")) return;
            fetch(`/campaigns/${encodeURIComponent(campaignTitleFromItems)}/delete_item/${itemId}`, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => {
                if (!response.ok) throw new Error("Ошибка сети при удалении предмета");
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    const row = this.closest("tr") || this.closest(".item-card");
                    if (row) row.remove();
                    alert("Предмет удален");
                } else {
                    alert("Ошибка: " + (data.message || "Не удалось удалить предмет"));
                }
            })
            .catch(err => {
                console.error("Ошибка запроса на удаление предмета:", err);
                alert("Произошла ошибка при удалении предмета");
            });
        });
    });

    const monsterDeleteButtons = document.querySelectorAll(".monster-delete-btn[data-monster-id]");
    const monsterContainer = document.getElementById("monsters-container");
    let campaignTitleFromMonsters = "";
    if (monsterContainer) {
        campaignTitleFromMonsters = monsterContainer.dataset?.campaignTitle || "";
    }
    if (!campaignTitleFromMonsters && monsterDeleteButtons.length > 0) {
        console.warn("Контейнер с data-campaign-title не найден для монстров");
        return;
    }
    monsterDeleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            const monsterId = this.dataset.monsterId || this.getAttribute("data-monster-id");
            if (!campaignTitleFromMonsters) {
                alert("Не удалось получить название кампании");
                return;
            }
            if (!confirm("Вы уверены, что хотите удалить этого монстра?")) return;
            fetch(`/campaigns/${encodeURIComponent(campaignTitleFromMonsters)}/delete_monster/${monsterId}`, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => {
                if (!response.ok) throw new Error("Ошибка сети при удалении монстра");
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    const row = this.closest("tr") || this.closest(".monster-card");
                    if (row) row.remove();
                    alert("Монстр удален");
                } else {
                    alert("Ошибка: " + (data.message || "Не удалось удалить монстра"));
                }
            })
            .catch(err => {
                console.error("Ошибка запроса на удаление монстра:", err);
                alert("Произошла ошибка при удалении монстра");
            });
        });
    });

    const locationDeleteButtons = document.querySelectorAll(".location-delete-btn[data-location-id]");
    const locationContainer = document.getElementById("locations-container");
    let campaignTitleFromLocations = "";
    if (locationContainer) {
        campaignTitleFromLocations = locationContainer.dataset?.campaignTitle || "";
    }
    if (!campaignTitleFromLocations && locationDeleteButtons.length > 0) {
        console.warn("Контейнер с data-campaign-title не найден для локаций");
        return;
    }
    locationDeleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            const locationId = this.dataset.locationId || this.getAttribute("data-location-id");
            if (!campaignTitleFromLocations) {
                alert("Не удалось получить название кампании");
                return;
            }
            if (!confirm("Вы уверены, что хотите удалить эту локацию?")) return;
            fetch(`/campaigns/${encodeURIComponent(campaignTitleFromLocations)}/delete_location/${locationId}`, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => {
                if (!response.ok) throw new Error("Ошибка сети при удалении локации");
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    const row = this.closest("tr") || this.closest(".location-card");
                    if (row) row.remove();
                    alert("Локация удалена");
                } else {
                    alert("Ошибка: " + (data.message || "Не удалось удалить локацию"));
                }
            })
            .catch(err => {
                console.error("Ошибка запроса на удаление локации:", err);
                alert("Произошла ошибка при удалении локации");
            });
        });
    });

    const eventDeleteButtons = document.querySelectorAll(".event-delete-btn[data-event-id]");
    const eventContainer = document.getElementById("events-container");
    let campaignTitleFromEvents = "";
    if (eventContainer) {
        campaignTitleFromEvents = eventContainer.dataset?.campaignTitle || "";
    }
    if (!campaignTitleFromEvents && eventDeleteButtons.length > 0) {
        console.warn("Контейнер с data-campaign-title не найден для событий");
        return;
    }
    eventDeleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            const eventId = this.dataset.eventId || this.getAttribute("data-event-id");
            if (!campaignTitleFromEvents) {
                alert("Не удалось получить название кампании");
                return;
            }
            if (!confirm("Вы уверены, что хотите удалить это событие?")) return;
            fetch(`/campaigns/${encodeURIComponent(campaignTitleFromEvents)}/delete_event/${eventId}`, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => {
                if (!response.ok) throw new Error("Ошибка сети при удалении события");
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    const row = this.closest("tr") || this.closest(".event-card");
                    if (row) row.remove();
                    alert("Событие удалено");
                } else {
                    alert("Ошибка: " + (data.message || "Не удалось удалить событие"));
                }
            })
            .catch(err => {
                console.error("Ошибка запроса на удаление события:", err);
                alert("Произошла ошибка при удалении события");
            });
        });
    });

    const campaignDeleteButtons = document.querySelectorAll(".campaign-delete-btn[data-campaign-title]");
    const campaignsContainer = document.getElementById("campaigns-container");

    let campaignPageTitle = "";
    if (campaignsContainer) {
        campaignPageTitle = campaignsContainer.dataset?.campaignTitle || "";
    }

    campaignDeleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            const campaignTitle = this.dataset.campaignTitle || this.getAttribute("data-campaign-title");

            if (!campaignTitle) {
                alert("Название кампании не найдено");
                return;
            }

            if (!confirm(`Вы уверены, что хотите удалить кампанию "${campaignTitle}"? Это удалит всех персонажей, НПЦ, монстров, предметы и другие данные.`)) return;

            fetch(`/campaigns/${encodeURIComponent(campaignTitle)}/delete_campaign`, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => {
                if (!response.ok) throw new Error("Ошибка сети при удалении кампании");
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    const card = this.closest(".campaign-card");
                    if (card) card.remove();
                    alert("Кампания удалена");
                    window.location.href = "/campaigns";
                } else {
                    alert("Ошибка: " + (data.message || "Не удалось удалить кампанию"));
                }
            })
            .catch(err => {
                console.error("Ошибка запроса на удаление кампании:", err);
                alert("Произошла ошибка при удалении кампании");
            });
        });
    });
});