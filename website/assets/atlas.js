(async () => {
  const root = document.querySelector("#atlas");
  if (!root) return;
  const es = document.body.dataset.lang === "es";
  const T = es ? {
    all: "Todos los parsers", runnable: "ejecutables", verified: "verificados", shown: (n, m) => `${n} de ${m} parsers`,
    cols: ["", "Rango", "Paquete", "Familia", "API de entrada", "Adopción", "Enlaces"],
    guide: "guía", harness: "harness", docs: "docs", ranking: "ranking", evidence: "evidencia", cellGuide: "notas completas de la búsqueda (en inglés)",
    std: "estándar", none: "Ningún parser coincide.", in: "en", leads: (n) => `${n} pistas sin resolver`,
    bench: "Abrir en el banco →", more: (n) => `Mostrar los ${n}`,
  } : {
    all: "All parsers", runnable: "runnable", verified: "verified", shown: (n, m) => `${n} of ${m} parsers`,
    cols: ["", "Rank", "Package", "Family", "Input API", "Adoption", "Links"],
    guide: "guide", harness: "harness", docs: "docs", ranking: "ranking", evidence: "evidence", cellGuide: "full search notes",
    std: "standard", none: "No parser matches.", in: "in", leads: (n) => `${n} unresolved leads`,
    bench: "Open in the bench →", more: (n) => `Show all ${n}`,
  };
  const METRIC_ES = {
    "Downloads": "descargas", "90-day downloads": "descargas en 90 días", "Imported by packages": "paquetes que lo importan",
    "Last-month downloads": "descargas del último mes", "Direct dependents": "dependientes directos",
    "Repository stars": "estrellas del repositorio", "Lifetime Composer downloads": "descargas totales en Composer",
    "Homebrew requested installs": "instalaciones solicitadas en Homebrew", "Primary GitHub stars": "estrellas en GitHub",
    "Lifetime downloads": "descargas totales", "Homebrew requested installs (365d)": "instalaciones solicitadas en Homebrew (365 días)",
    "Requested installs (365d)": "instalaciones solicitadas (365 días)", "Stars": "estrellas",
    "Packagist lifetime downloads": "descargas totales en Packagist",
    "Debian installations (popcon)": "instalaciones en Debian (popcon)",
    "Imported by (pkg.go.dev)": "importado por (pkg.go.dev)",
    "Direct dependents (deps.dev)": "dependientes directos (deps.dev)",
    "npm downloads (last month)": "descargas en npm (último mes)",
    "PyPI downloads (last month)": "descargas en PyPI (último mes)",
    "crates.io downloads (90 days)": "descargas en crates.io (90 días)",
    "Packagist downloads (all time)": "descargas en Packagist (totales)",
    "Homebrew installs (365 days)": "instalaciones en Homebrew (365 días)",
    "GitHub stars": "estrellas en GitHub",
    "Debian development-package installations (popcon)": "instalaciones del paquete de desarrollo en Debian (popcon)",
  };
  const metricName = (m) => !m ? "" : es ? (METRIC_ES[m] || m) : m;
  const metricValue = (v) => es && /^[\d,]+$/.test(v || "") ? v.replace(/,/g, ".") : v;
  const plural = (n, one, many) => `${n} ${n === 1 ? one : many}`;
  const cellSummary = (cell) => {
    const inCell = catalog.parsers.filter((p) => p.format === cell.format && p.ecosystem === cell.ecosystem);
    const families = new Set(inCell.map((p) => p.family)).size;
    const metric = metricName(inCell.find((p) => p.popularityMetric)?.popularityMetric);
    if (es) return [
      `${plural(cell.verified, "paquete verificado", "paquetes verificados")} de ${plural(families, "familia de parsers", "familias de parsers")}`
        + (cell.standard ? ` y ${plural(cell.standard, "API de la biblioteca estándar", "APIs de la biblioteca estándar")}` : "") + ".",
      `${cell.runnable} ${cell.runnable === 1 ? "tiene" : "tienen"} un harness ejecutable.`,
      metric ? `Métrica de adopción: ${metric}.` : "",
      cell.unresolved ? `Quedan ${plural(cell.unresolved, "pista de búsqueda abierta", "pistas de búsqueda abiertas")}.` : "",
    ].filter(Boolean).join(" ");
    return [
      `${plural(cell.verified, "verified package", "verified packages")} from ${plural(families, "parser family", "parser families")}`
        + (cell.standard ? ` and ${plural(cell.standard, "standard-library API", "standard-library APIs")}` : "") + ".",
      `${cell.runnable} ${cell.runnable === 1 ? "has" : "have"} a runnable harness.`,
      metric ? `Adoption metric: ${metric.charAt(0).toLowerCase() + metric.slice(1)}.` : "",
      cell.unresolved ? `${plural(cell.unresolved, "search lead is", "search leads are")} still open.` : "",
    ].filter(Boolean).join(" ");
  };
  const ECO = { c: "C", cpp: "C++", go: "Go", java: "Java", javascript: "JavaScript", python: "Python", rust: "Rust", php: "PHP" };
  const catalog = await fetch(root.dataset.catalog).then((r) => r.json());
  const formats = catalog.formats;
  const ecos = catalog.ecosystems;
  const label = Object.fromEntries(formats.map((f) => [f.id, f.label]));
  const cellOf = Object.fromEntries(catalog.cells.map((c) => [`${c.format}|${c.ecosystem}`, c]));
  const rows = [...catalog.parsers, ...catalog.standardTargets.map((s) => ({ ...s, standard: true }))];
  const maxRun = Math.max(...catalog.cells.map((c) => c.runnable));

  const params = new URLSearchParams(location.search);
  const state = {
    format: label[params.get("format")] ? params.get("format") : null,
    ecosystem: ecos.includes(params.get("ecosystem")) ? params.get("ecosystem") : null,
    q: params.get("q") || "",
    runnable: params.get("runnable") === "1",
    expanded: false,
  };

  const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const table = root.querySelector(".matrix");
  table.innerHTML = `<thead><tr><th></th>${ecos.map((e) => `<th scope="col"><button type="button" data-eco="${e}">${ECO[e]}</button></th>`).join("")}</tr></thead>
    <tbody>${formats.map((f) => `<tr><th scope="row"><button type="button" data-fmt="${f.id}">${f.label}</button></th>${ecos.map((e) => {
      const c = cellOf[`${f.id}|${e}`];
      const v = Math.round(12 + 78 * c.runnable / maxRun);
      return `<td><button type="button" data-cell="${f.id}|${e}" class="${v > 62 ? "hi" : ""}" style="--v:${v}" aria-label="${f.label} ${T.in} ${ECO[e]}: ${c.runnable} ${T.runnable}, ${c.verified + c.standard} ${T.verified}"><b>${c.runnable}</b><small>/${c.verified + c.standard}</small></button></td>`;
    }).join("")}</tr>`).join("")}</tbody>`;

  table.addEventListener("click", (event) => {
    const b = event.target.closest("button"); if (!b) return;
    if (b.dataset.cell) {
      const [f, e] = b.dataset.cell.split("|");
      const same = state.format === f && state.ecosystem === e;
      state.format = same ? null : f; state.ecosystem = same ? null : e;
    } else if (b.dataset.fmt) {
      const same = state.format === b.dataset.fmt && !state.ecosystem;
      state.format = same ? null : b.dataset.fmt; state.ecosystem = null;
    } else if (b.dataset.eco) {
      const same = state.ecosystem === b.dataset.eco && !state.format;
      state.ecosystem = same ? null : b.dataset.eco; state.format = null;
    }
    state.expanded = false;
    update();
    root.querySelector(".atlas-list").scrollIntoView({ behavior: "smooth", block: "start" });
  });
  const search = root.querySelector(".search");
  search.value = state.q;
  search.addEventListener("input", () => { state.q = search.value; state.expanded = false; update(); });
  const runBox = root.querySelector("[data-runnable]");
  runBox.checked = state.runnable;
  runBox.addEventListener("change", () => { state.runnable = runBox.checked; update(); });

  function update() {
    const q = new URLSearchParams();
    if (state.format) q.set("format", state.format);
    if (state.ecosystem) q.set("ecosystem", state.ecosystem);
    if (state.q) q.set("q", state.q);
    if (state.runnable) q.set("runnable", "1");
    history.replaceState(null, "", `${q.toString() ? "?" + q : location.pathname}`);
    table.querySelectorAll("[data-cell]").forEach((b) => {
      const [f, e] = b.dataset.cell.split("|");
      const on = (!state.format || state.format === f) && (!state.ecosystem || state.ecosystem === e) && (state.format || state.ecosystem);
      b.setAttribute("aria-pressed", String(Boolean(on)));
    });

    const needle = state.q.trim().toLowerCase();
    const scoped = rows.filter((p) => (!state.format || p.format === state.format)
      && (!state.ecosystem || p.ecosystem === state.ecosystem));
    const shown = scoped.filter((p) => (!state.runnable || p.projectUrl)
      && (!needle || `${p.name} ${p.family} ${p.inputApi} ${p.license || ""}`.toLowerCase().includes(needle)));

    let title = T.all;
    if (state.format && state.ecosystem) title = `${label[state.format]} ${T.in} ${ECO[state.ecosystem]}`;
    else if (state.format) title = label[state.format];
    else if (state.ecosystem) title = ECO[state.ecosystem];
    const cell = state.format && state.ecosystem ? cellOf[`${state.format}|${state.ecosystem}`] : null;
    const benchQ = new URLSearchParams();
    benchQ.set("f", state.format || formats.map((f) => f.id).join(","));
    if (state.ecosystem) benchQ.set("e", state.ecosystem);
    const head = `<div class="cell-head"><h2>${esc(title)}</h2><span class="label" style="margin:0">${T.shown(shown.length, scoped.length)}</span></div>
      ${cell ? `<p class="cell-note">${esc(cellSummary(cell))}</p>
        <p class="cell-links"><a href="${cell.rankingUrl}" rel="noopener">${T.ranking} ↗</a><a href="${cell.evidenceUrl}" rel="noopener">${T.evidence} ↗</a><a href="${cell.cellGuideUrl}" rel="noopener">${T.cellGuide} ↗</a><a href="${document.body.dataset.localeRoot}bench/?${benchQ}">${T.bench}</a></p>` :
        `<p class="cell-links"><a href="${document.body.dataset.localeRoot}bench/?${benchQ}">${T.bench}</a></p>`}`;
    if (!shown.length) { root.querySelector(".atlas-list").innerHTML = head + `<p>${T.none}</p>`; return; }
    const limit = state.expanded ? shown.length : 200;
    const body = shown.slice(0, limit).map((p) => `<tr>
      <td><span class="dot${p.projectUrl ? " on" : ""}" title="${p.projectUrl ? T.runnable : T.verified}"></span></td>
      <td class="num">${esc(p.rank || "")}</td>
      <td>${p.repository || p.registryUrl ? `<a class="pkg" href="${esc(p.repository || p.registryUrl)}" rel="noopener">${esc(p.name)}</a>` : `<span class="pkg">${esc(p.name)}</span>`} <span class="rel">${esc(p.version)}</span>${p.standard ? ` <span class="tag std">${T.std}</span>` : ""}${state.format && state.ecosystem ? "" : `<br><span class="rel">${esc(label[p.format])} · ${ECO[p.ecosystem]}</span>`}</td>
      <td>${esc(p.family)}</td>
      <td class="api" title="${esc(p.inputApi)}">${esc(p.inputApi)}</td>
      <td>${p.metricValue ? `${esc(metricValue(p.metricValue))}<br><span class="rel">${esc(metricName(p.popularityMetric))}</span>` : ""}</td>
      <td style="white-space:nowrap"><a href="${esc(p.guideUrl)}" rel="noopener">${T.guide}</a>${p.projectUrl && !p.standard ? ` · <a href="${esc(p.projectUrl)}" rel="noopener">${T.harness}</a>` : ""} · <a href="${esc(p.documentation)}" rel="noopener">${T.docs}</a>${p.registryUrl ? ` · <a href="${esc(p.registryUrl)}" rel="noopener">${esc(p.registryName)}</a>` : ""}</td></tr>`).join("");
    const more = shown.length > limit ? `<p class="more"><button type="button" class="chip" data-more>${T.more(shown.length)}</button></p>` : "";
    root.querySelector(".atlas-list").innerHTML = head + `<div class="table-scroll"><table class="t"><thead><tr>${T.cols.map((c) => `<th>${c}</th>`).join("")}</tr></thead><tbody>${body}</tbody></table></div>${more}`;
    const m = root.querySelector("[data-more]");
    if (m) m.addEventListener("click", () => { state.expanded = true; update(); });
  }
  update();
})();
