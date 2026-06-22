// app.js
document.addEventListener("DOMContentLoaded", () => {

    // Auto scroll conversation
    const historyCard = document.querySelector(".history-card");

    if (historyCard) {
        historyCard.scrollTop = historyCard.scrollHeight;
    }

    // Loading Spinner
    const spinner = document.getElementById("loading-spinner");
    const uploadForm = document.querySelector("form[action='/upload']");

    if (spinner) {
        spinner.style.display = "none";
    }

    if (uploadForm && spinner) {

        uploadForm.addEventListener("submit", () => {

            spinner.style.display = "flex";

        });

    }

});