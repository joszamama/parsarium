(() => {
  const toggle = document.querySelector("#mobile-menu-toggle");
  const menu = document.querySelector("#mobile-nav");
  if (!toggle || !menu) return;
  const close = () => { menu.hidden = true; toggle.setAttribute("aria-expanded", "false"); };
  toggle.addEventListener("click", () => {
    const open = menu.hidden;
    menu.hidden = !open;
    toggle.setAttribute("aria-expanded", String(open));
  });
  menu.addEventListener("click", (event) => { if (event.target.closest("a")) close(); });
  document.addEventListener("keydown", (event) => { if (event.key === "Escape") close(); });
  matchMedia("(min-width: 801px)").addEventListener("change", (event) => { if (event.matches) close(); });
})();
