document.addEventListener("DOMContentLoaded", () => {
    const deleteButtons = document.querySelectorAll(".delete-btn");

    if (deleteButtons.length === 0) return;

    const playersList = document.querySelector(".players-list");
    const campaignTitle = playersList.dataset.campaignTitle;

    if (!campaignTitle) {
        console.error("Название кампании не найдено");
        alert("Ошибка: кампания не загружена корректно");
        return;
    }

    deleteButtons.forEach(button => {
        button.addEventListener("click", async (event) => {
            const playerName = event.target.dataset.playerName;

            if (!playerName) {
                alert("Имя игрока не определено");
                return;
            }

            if (!confirm(`Вы уверены, что хотите удалить игрока "${playerName}"?`)) return;

            try {
                const response = await fetch(`/campaigns/${campaignTitle}/delete_player/${playerName}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    }
                });

                const result = await response.json();

                if (result.success) {
                    event.target.closest(".player-card").remove();
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
});