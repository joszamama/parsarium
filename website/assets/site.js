(() => {
  document.documentElement.classList.add("js");
  const lang = document.body.dataset.lang;
  // Keep the query and hash when switching language.
  document.querySelectorAll("a.lang").forEach((link) => {
    link.addEventListener("click", () => {
      const target = new URL(link.href);
      target.search = location.search;
      target.hash = location.hash;
      link.href = target.href;
    });
  });

  const toggle = document.querySelector(".menu");
  const nav = document.querySelector("#nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = !nav.classList.contains("open");
      nav.classList.toggle("open", open);
      toggle.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") { nav.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); }
    });
  }

  // Copy buttons on every code block marked data-copy.
  const label = lang === "es" ? ["Copiar", "Copiado"] : ["Copy", "Copied"];
  window.parsariumCopy = (pre) => {
    if (pre.parentElement.classList.contains("copy-wrap")) return;
    const wrap = document.createElement("div");
    wrap.className = "copy-wrap";
    pre.replaceWith(wrap);
    wrap.append(pre);
    const button = document.createElement("button");
    button.type = "button";
    button.className = "copy";
    button.textContent = label[0];
    button.addEventListener("click", async () => {
      const text = [...pre.childNodes].map((node) =>
        node.classList && node.classList.contains("p") ? "" : node.textContent).join("");
      try { await navigator.clipboard.writeText(text.trim()); button.textContent = label[1]; }
      catch { button.textContent = "×"; }
      setTimeout(() => { button.textContent = label[0]; }, 1400);
    });
    wrap.append(button);
  };
  document.querySelectorAll("pre[data-copy]").forEach(window.parsariumCopy);

  // Manual progress, kept in this browser only.
  const store = {
    get(key) { try { return localStorage.getItem(`parsarium:${key}`); } catch { return null; } },
    set(key, value) { try { localStorage.setItem(`parsarium:${key}`, value); } catch { /* storage unavailable */ } },
  };
  window.parsariumStore = store;
  window.parsariumProgress = () => {
    document.querySelectorAll(".toc a[data-slug]").forEach((a) => {
      const slug = a.dataset.slug;
      const quiz = store.get(`quiz:${slug}`);
      const total = Number(a.dataset.ex || 0);
      let done = 0;
      for (let i = 1; i <= total; i++) if (store.get(`ex:${slug}:${i}`) === "1") done++;
      a.querySelector(".prog")?.remove();
      if (!quiz && !done) return;
      const span = document.createElement("span");
      span.className = "prog";
      const parts = [];
      if (quiz) parts.push(`${lang === "es" ? "test" : "quiz"} ${quiz}`);
      if (done) parts.push(`${lang === "es" ? "ejercicios" : "exercises"} ${done}/${total}`);
      span.textContent = parts.join(" · ");
      a.append(span);
    });
  };
  window.parsariumProgress();
})();
