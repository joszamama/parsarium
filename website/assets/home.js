(() => {
  // Highlight one PNG region at a time from the legend or the bytes.
  const dump = document.querySelector(".hexdump");
  const legend = document.querySelector(".legend");
  if (dump && legend) {
    const set = (region) => {
      dump.classList.toggle("focus", Boolean(region));
      dump.querySelectorAll("[data-r]").forEach((el) => el.classList.toggle("on", el.dataset.r === region));
      legend.querySelectorAll("li").forEach((li) => li.classList.toggle("on", li.dataset.r === region));
    };
    const over = (event) => { const el = event.target.closest("[data-r]"); set(el ? el.dataset.r : null); };
    dump.addEventListener("mouseover", over);
    legend.addEventListener("mouseover", over);
    dump.addEventListener("mouseleave", () => set(null));
    legend.addEventListener("mouseleave", () => set(null));
  }

  // Duplicate the reader list so the roll loops without a jump.
  const list = document.querySelector(".readers ol");
  if (list && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const count = list.children.length;
    list.innerHTML += list.innerHTML;
    [...list.children].slice(count).forEach((li) => li.setAttribute("aria-hidden", "true"));
    list.style.setProperty("--roll", `${Math.max(40, count * 1.1)}s`);
  }
})();
