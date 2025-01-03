document.addEventListener("DOMContentLoaded", () => {
    const modalContent = document.getElementById("resultadoContent");

    document.querySelectorAll(".view-results").forEach(button => {
        button.addEventListener("click", function () {
            const enqueteId = this.getAttribute("data-enquete-id");
            modalContent.innerHTML = "<p>Carregando resultados...</p>";

            fetch(`/enquetes/resultado/${enqueteId}/`)
                .then(response => {
                    if (!response.ok) throw new Error("Erro ao carregar os resultados.");
                    return response.json();
                })
                .then(data => {
                    modalContent.innerHTML = data.results; // Insere os resultados na modal
                })
                .catch(error => {
                    console.error(error);
                    modalContent.innerHTML = "<p>Erro ao carregar os resultados. Tente novamente mais tarde.</p>";
                });
        });
    });
});
