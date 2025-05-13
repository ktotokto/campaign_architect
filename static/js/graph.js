document.addEventListener("DOMContentLoaded", function () {
    const campaignTitle = document.getElementById("mynetwork")?.dataset?.campaignTitle || "";

    if (!campaignTitle) {
        console.warn("Название кампании не найдено для графа");
        return;
    }

    async function loadGraph() {
        try {
            const res = await fetch(`/api/campaigns/${encodeURIComponent(campaignTitle)}/graph`);
            if (!res.ok) throw new Error("Ошибка сети при загрузке данных");

            const data = await res.json();

            const nodes = new vis.DataSet(data.nodes);
            const edges = new vis.DataSet(data.edges);

            const container = document.getElementById("mynetwork");
            const options = {
                nodes: {
                    shape: 'box',
                    color: { background: '#3a250f', border: '#f5d742' },
                    font: { color: '#e0d8b0' }
                },
                edges: {
                    color: '#f5d742',
                    arrows: { to: true },
                    smooth: { enabled: true, type: 'curvedCW' },
                    font: { color: '#f5d742', size: 14 }
                },
                physics: {
                    enabled: true,
                    stabilization: true
                }
            };

            const network = new vis.Network(container, { nodes, edges }, options);

            network.on("click", function (params) {
                if (params.event && params.event.target && params.event.target.classList.contains("vis-edge")) {
                    const edgeId = params.event.target.dataset?.id;

                    if (!edgeId) {
                        console.warn("ID связи не найден");
                        return;
                    }

                    if (!confirm("Удалить эту связь?")) return;

                    fetch(`/api/campaigns/${campaignTitle}/delete_connection/${edgeId}`, {
                        method: "DELETE",
                        headers: { "X-Requested-With": "XMLHttpRequest" }
                    })
                    .then(response => {
                        if (!response.ok) throw new Error("Ошибка сети при удалении связи");
                        return response.json();
                    })
                    .then(result => {
                        if (result.success) {
                            edges.remove(edgeId);
                            alert("Связь удалена");
                        } else {
                            alert("Ошибка: " + result.message || "Не удалось удалить связь");
                        }
                    })
                    .catch(err => {
                        console.error("Ошибка запроса на удаление:", err);
                        alert("Произошла ошибка при удалении связи");
                    });
                }
            });

            const fromSelect = document.getElementById("from-event");
            const toSelect = document.getElementById("to-event");

            data.nodes.forEach(node => {
                fromSelect.add(new Option(node.label, node.id));
                toSelect.add(new Option(node.label, node.id));
            });

            document.getElementById("connection-form").addEventListener("submit", async (e) => {
                e.preventDefault();

                const fromId = parseInt(fromSelect.value);
                const toId = parseInt(toSelect.value);
                const label = document.getElementById("connection-label").value.trim();

                const response = await fetch(`/api/campaigns/${encodeURIComponent(campaignTitle)}/add_connection`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ from: fromId, to: toId, label: label })
                });

                const result = await response.json();
                if (result.success) {
                    edges.add(result.edge);
                    alert("Связь добавлена");
                } else {
                    alert("Ошибка: " + result.message || "Не удалось добавить связь");
                }
            });
        } catch (err) {
            console.error("Ошибка при загрузке графа:", err);
            alert("Не удалось загрузить граф событий");
        }
    }

    window.addEventListener("load", () => {
        const container = document.getElementById("mynetwork");
        if (container) loadGraph();
    });
});