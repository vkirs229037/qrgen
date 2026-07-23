const container = document.querySelector("main")

container.addEventListener("click", (event) => {
    if (event.target.classList.contains("alert")) {
        event.target.remove();
    }
})