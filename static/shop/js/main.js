document.addEventListener("DOMContentLoaded", () => {
    const currentPath = window.location.pathname;
    const links = document.querySelectorAll(".nav a");

    links.forEach((link) => {
        const linkPath = new URL(link.href).pathname;
        const isHome = linkPath === "/" && currentPath === "/";
        const isSection = linkPath !== "/" && currentPath.startsWith(linkPath);

        if (isHome || isSection) {
            link.classList.add("active");
        }
    });
});
