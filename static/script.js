document.addEventListener("DOMContentLoaded", function() {
    let highlights = document.querySelectorAll(".highlight");
    highlights.forEach(el => {
        el.style.opacity = "0";
        setTimeout(() => {
            el.style.opacity = "1";
            el.style.transition = "opacity 1s ease-in-out";
        }, 500);
    });
});
