const $ = (selector) => document.querySelector(selector);
const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
}[char]));
const safeUrl = (value) => {
  try {
    const url = new URL(value, location.href);
    return ["https:", "http:"].includes(url.protocol) ? url.href : "#";
  } catch { return "#"; }
};
const ecoLabel = { c: "C", cpp: "C++", go: "Go", java: "Java", javascript: "JavaScript", python: "Python", rust: "Rust", php: "PHP" };
const formatGlyphs = {
  png: '<rect x="54" y="16" width="88" height="70" rx="4" fill="#fff8e8" stroke="#14251f" stroke-width="2"/><rect x="63" y="25" width="70" height="52" fill="#f5efdf"/><rect x="63" y="25" width="35" height="26" fill="#fa7454"/><rect x="98" y="51" width="35" height="26" fill="#b9db79"/><circle cx="113" cy="36" r="10" fill="#14251f"/><path d="M63 77 83 52l18 25" fill="none" stroke="#14251f" stroke-width="3"/>',
  zip: '<rect x="55" y="19" width="87" height="68" rx="5" fill="#fff6e5" stroke="#14251f" stroke-width="2"/><path d="M55 41h87M55 64h87" stroke="#14251f" stroke-width="2"/><path d="M88 19v68" stroke="#14251f" stroke-width="2" stroke-dasharray="5 4"/><rect x="79" y="45" width="18" height="15" rx="2" fill="#ff6b42" stroke="#14251f" stroke-width="2"/>',
  mp4: '<rect x="48" y="19" width="100" height="68" rx="5" fill="#14251f"/><rect x="58" y="30" width="80" height="46" rx="2" fill="#f7e7be"/><path d="m94 39 20 14-20 14Z" fill="#ff6b42"/><path d="M61 19v10m17-10v10m17-10v10m17-10v10m17-10v10" stroke="#f7e7be" stroke-width="4"/>',
  wav: '<path d="M40 52h15m4-16v32m9-43v54m9-36v18m9-40v62m9-46v28m9-34v40m9-22v8m9-30v50m9-38v26m9-17h16" fill="none" stroke="#14251f" stroke-width="4" stroke-linecap="round"/><circle cx="98" cy="52" r="47" fill="none" stroke="#14251f" stroke-width="2" stroke-dasharray="3 5"/>',
  pdf: '<path d="M62 14h59l17 18v58H62Z" fill="#fff8ed" stroke="#14251f" stroke-width="2"/><path d="M121 14v18h17" fill="#f5ceb5" stroke="#14251f" stroke-width="2"/><path d="M72 47h56M72 56h47M72 65h54M72 74h27" stroke="#14251f" stroke-width="3"/><rect x="75" y="22" width="23" height="13" fill="#ff6b42"/>',
  svg: '<circle cx="98" cy="52" r="39" fill="#fff7e4" stroke="#14251f" stroke-width="2"/><path d="M62 70q28-56 68 0" fill="none" stroke="#ff6b42" stroke-width="5"/><circle cx="62" cy="70" r="6" fill="#14251f"/><circle cx="98" cy="27" r="6" fill="#14251f"/><circle cx="130" cy="70" r="6" fill="#14251f"/>',
  http11: '<rect x="47" y="19" width="103" height="69" rx="4" fill="#fff8ed" stroke="#14251f" stroke-width="2"/><path d="M47 34h103" stroke="#14251f" stroke-width="2"/><circle cx="57" cy="27" r="3" fill="#ff6b42"/><circle cx="67" cy="27" r="3" fill="#e3c560"/><circle cx="77" cy="27" r="3" fill="#9ac466"/><path d="M59 47h30m-30 11h73M59 69h56" stroke="#14251f" stroke-width="3"/><rect x="102" y="42" width="29" height="11" fill="#b7da81"/>',
  ascii_ply: '<path d="m96 15 45 70H51Z" fill="#f7ead0" stroke="#14251f" stroke-width="2"/><path d="m96 15 6 42-51 28m51-28 39 28" fill="none" stroke="#14251f" stroke-width="2"/><circle cx="96" cy="15" r="5" fill="#ff6b42"/><circle cx="102" cy="57" r="5" fill="#ff6b42"/><circle cx="51" cy="85" r="5" fill="#ff6b42"/><circle cx="141" cy="85" r="5" fill="#ff6b42"/>',
  ascii_pnm: '<rect x="54" y="17" width="92" height="72" fill="#fff8ea" stroke="#14251f" stroke-width="2"/><path d="M77 17v72m23-72v72m23-72v72M54 41h92M54 65h92" stroke="#14251f" stroke-width="2"/><rect x="55" y="18" width="21" height="22" fill="#ff6b42"/><rect x="101" y="42" width="21" height="22" fill="#d6ee7f"/><rect x="124" y="66" width="21" height="22" fill="#a6c9e5"/>',
  mp3_id3v2: '<circle cx="98" cy="52" r="42" fill="#14251f"/><circle cx="98" cy="52" r="27" fill="none" stroke="#6f846f" stroke-width="2"/><circle cx="98" cy="52" r="13" fill="#ff6b42"/><circle cx="98" cy="52" r="4" fill="#fff8e8"/><path d="m130 17 17 20" stroke="#14251f" stroke-width="5" stroke-linecap="round"/><circle cx="147" cy="38" r="5" fill="#14251f"/>'
};
const artColors = {
  png:"#f9d7b8", zip:"#c7d9f0", mp4:"#e4ccf0", wav:"#d5ebaa", pdf:"#ffd5c4",
  svg:"#bfe3dd", http11:"#e8dfa4", ascii_ply:"#e8cdb3", ascii_pnm:"#d6e2ff", mp3_id3v2:"#e9d0d8"
};

let catalog;
const pageSize = 18;
let visible = pageSize;
function formatLabel(id) { return catalog.formats.find((format) => format.id === id)?.label ?? id; }
function announceCopy(button, label) {
  const old = button.textContent;
  button.textContent = label;
  setTimeout(() => { button.textContent = old; }, 1500);
}
async function copyText(value, button) {
  try { await navigator.clipboard.writeText(value); announceCopy(button, "Copied ✓"); }
  catch { announceCopy(button, "Copy unavailable"); }
}

function renderFormats() {
  $("#format-grid").innerHTML = catalog.formats.map((format) => `
    <button class="format-card" type="button" data-format="${escapeHtml(format.id)}" aria-label="Explore ${escapeHtml(format.label)} parsers">
      <span class="format-art" style="background:${artColors[format.id]}"><svg viewBox="0 0 196 104" aria-hidden="true">${formatGlyphs[format.id]}</svg></span>
      <span class="format-content"><span class="format-category">${escapeHtml(format.category)}</span><span class="format-name">${escapeHtml(format.label)} <span aria-hidden="true">↗</span></span><span class="format-count"><b>${format.verified}</b> verified · <b>${format.runnable}</b> runnable</span></span>
    </button>`).join("");
  $("#format-grid").addEventListener("click", (event) => {
    const button = event.target.closest("[data-format]");
    if (!button) return;
    $("#format-filter").value = button.dataset.format;
    $("#ecosystem-filter").value = "";
    $("#search").value = "";
    $("#runnable-filter").checked = false;
    visible = pageSize;
    renderAtlas();
    $("#atlas").scrollIntoView({ behavior: "smooth" });
  });
}
function currentFilters() {
  return {
    format: $("#format-filter").value,
    ecosystem: $("#ecosystem-filter").value,
    query: $("#search").value.trim().toLocaleLowerCase(),
    runnable: $("#runnable-filter").checked
  };
}
function updateUrl(filters) {
  const params = new URLSearchParams();
  if (filters.format) params.set("format", filters.format);
  if (filters.ecosystem) params.set("ecosystem", filters.ecosystem);
  if (filters.query) params.set("q", filters.query);
  if (filters.runnable) params.set("runnable", "1");
  const url = `${location.pathname}${params.size ? `?${params}` : ""}${location.hash}`;
  history.replaceState(null, "", url);
}
function parserCard(parser) {
  const project = parser.projectUrl ? `<a href="${safeUrl(parser.projectUrl)}" target="_blank" rel="noopener noreferrer">Harness ↗</a>` : "";
  return `<article class="parser-card-item">
    <div class="parser-meta"><span>${escapeHtml(formatLabel(parser.format))} / ${escapeHtml(ecoLabel[parser.ecosystem])}</span>${parser.projectUrl ? '<span class="runnable-badge">RUNNABLE</span>' : ""}</div>
    <h3>${escapeHtml(parser.name)}</h3><span class="parser-version">${escapeHtml(parser.version)} · ${escapeHtml(parser.license)} · scope: ${escapeHtml(parser.scope)}</span>
    <p class="parser-api"><strong>Input API:</strong> ${escapeHtml(parser.inputApi)}</p>
    <p class="parser-family">Family: ${escapeHtml(parser.family)}</p>
    <div class="parser-card-links"><a href="${safeUrl(parser.documentation)}" target="_blank" rel="noopener noreferrer">Docs ↗</a><a href="${safeUrl(parser.evidenceUrl)}" target="_blank" rel="noopener noreferrer">Evidence ↗</a>${project}</div>
  </article>`;
}
function renderAtlas() {
  const filters = currentFilters();
  const result = catalog.parsers.filter((parser) => {
    if (filters.format && parser.format !== filters.format) return false;
    if (filters.ecosystem && parser.ecosystem !== filters.ecosystem) return false;
    if (filters.runnable && !parser.projectUrl) return false;
    if (filters.query) {
      const haystack = [parser.name, parser.inputApi, parser.family, parser.scope, parser.version].join(" ").toLocaleLowerCase();
      if (!haystack.includes(filters.query)) return false;
    }
    return true;
  });
  const shown = result.slice(0, visible);
  $("#result-count").textContent = `Showing ${shown.length.toLocaleString()} of ${result.length.toLocaleString()} verified package paths`;
  $("#parser-grid").innerHTML = shown.length ? shown.map(parserCard).join("") : '<div class="empty-state">No verified parsers match those filters. Try another format, ecosystem, or search term.</div>';
  $("#load-more").hidden = shown.length >= result.length;
  const note = $("#cell-note");
  if (filters.format && filters.ecosystem) {
    const cell = catalog.cells.find((item) => item.format === filters.format && item.ecosystem === filters.ecosystem);
    note.hidden = false;
    note.innerHTML = `<strong>${escapeHtml(formatLabel(filters.format))} × ${escapeHtml(ecoLabel[filters.ecosystem])}</strong>
      <p>${cell.verified} verified third-party paths · ${cell.runnable} runnable harness${cell.runnable === 1 ? "" : "es"} · ${cell.standard} standard/runtime APIs · ${cell.unresolved} unresolved documentation leads.</p>
      <div class="cell-links"><a href="${safeUrl(cell.rankingUrl)}" target="_blank" rel="noopener noreferrer">Popularity ranking & search limits ↗</a>
      <a href="${safeUrl(cell.standardUrl)}" target="_blank" rel="noopener noreferrer">Standard API inventory ↗</a>
      ${cell.standardProjectUrl ? `<a href="${safeUrl(cell.standardProjectUrl)}" target="_blank" rel="noopener noreferrer">Standard API harness ↗</a>` : ""}</div>
      <details><summary>What remains uncertain</summary><p>${escapeHtml(cell.uncertainty)}</p></details>`;
  } else { note.hidden = true; note.innerHTML = ""; }
  updateUrl(filters);
}
function initAtlas() {
  $("#format-filter").insertAdjacentHTML("beforeend", catalog.formats.map((f) => `<option value="${escapeHtml(f.id)}">${escapeHtml(f.label)}</option>`).join(""));
  $("#ecosystem-filter").insertAdjacentHTML("beforeend", catalog.ecosystems.map((eco) => `<option value="${escapeHtml(eco)}">${escapeHtml(ecoLabel[eco])}</option>`).join(""));
  const initial = new URLSearchParams(location.search);
  if (catalog.formats.some((f) => f.id === initial.get("format"))) $("#format-filter").value = initial.get("format");
  if (catalog.ecosystems.includes(initial.get("ecosystem"))) $("#ecosystem-filter").value = initial.get("ecosystem");
  $("#search").value = initial.get("q") || "";
  $("#runnable-filter").checked = initial.get("runnable") === "1";
  ["format-filter", "ecosystem-filter", "runnable-filter"].forEach((id) => $(`#${id}`).addEventListener("change", () => { visible = pageSize; renderAtlas(); }));
  $("#search").addEventListener("input", () => { visible = pageSize; renderAtlas(); });
  $("#clear-filters").addEventListener("click", () => {
    $("#format-filter").value = ""; $("#ecosystem-filter").value = ""; $("#search").value = ""; $("#runnable-filter").checked = false;
    visible = pageSize; renderAtlas();
  });
  $("#load-more").addEventListener("click", () => { visible += pageSize; renderAtlas(); });
  document.addEventListener("keydown", (event) => {
    if (event.key === "/" && !["INPUT", "TEXTAREA", "SELECT"].includes(document.activeElement.tagName)) {
      event.preventDefault(); $("#search").focus(); $("#atlas").scrollIntoView();
    }
  });
  renderAtlas();
}
function selectCell(format, ecosystem) {
  $("#format-filter").value = format;
  $("#ecosystem-filter").value = ecosystem;
  $("#search").value = "";
  $("#runnable-filter").checked = false;
  visible = pageSize;
  renderAtlas();
  $("#atlas").scrollIntoView({ behavior: "smooth" });
}
function renderMatrix() {
  const map = new Map(catalog.cells.map((cell) => [`${cell.format}:${cell.ecosystem}`, cell]));
  let html = '<span></span>';
  html += catalog.ecosystems.map((eco) => `<span class="matrix-heading">${escapeHtml(ecoLabel[eco])}</span>`).join("");
  for (const format of catalog.formats) {
    html += `<span class="matrix-row-label">${escapeHtml(format.label)}</span>`;
    for (const eco of catalog.ecosystems) {
      const cell = map.get(`${format.id}:${eco}`);
      html += `<button class="matrix-cell ${cell.verified < 20 ? "low" : ""}" type="button" data-format="${escapeHtml(format.id)}" data-eco="${escapeHtml(eco)}" aria-label="${cell.verified} verified ${escapeHtml(format.label)} parsers in ${escapeHtml(ecoLabel[eco])}">${cell.verified}</button>`;
    }
  }
  $("#matrix").innerHTML = html;
  $("#matrix").addEventListener("click", (event) => {
    const button = event.target.closest(".matrix-cell");
    if (button) selectCell(button.dataset.format, button.dataset.eco);
  });
}
function renderDemo(index) {
  const demo = catalog.demos[index];
  $("#demo-tabs").querySelectorAll("button").forEach((button, buttonIndex) => {
    button.setAttribute("aria-selected", String(buttonIndex === index));
    button.tabIndex = buttonIndex === index ? 0 : -1;
  });
  $("#demo-panel").setAttribute("aria-labelledby", `demo-tab-${index}`);
  const hex = demo.hex.match(/.{1,47}(?: |$)/g)?.join("\n") ?? demo.hex;
  $("#demo-panel").innerHTML = `<div class="workbench-top"><span>VALID CONTROL / ${escapeHtml(formatLabel(demo.format))}</span><span class="workbench-lights" aria-hidden="true"><i></i><i></i><i></i></span></div>
    <div class="workbench-body"><div class="workbench-step">01 — INPUT BYTES</div>
      <div class="workbench-file"><strong>${escapeHtml(demo.control.split("/").pop())}</strong><span>${demo.bytes.toLocaleString()} bytes</span></div>
      <pre class="hex-view">${escapeHtml(hex)}${demo.bytes > 48 ? "\n…" : ""}</pre>
      <div class="parse-arrow">PARSED BY ${escapeHtml(demo.package)} ${escapeHtml(demo.release)}</div>
      <div class="workbench-step">02 — OBSERVED FORMAT-AWARE RESULT</div>
      <pre class="output-view">${escapeHtml(JSON.stringify(demo.expectedOutput, null, 2))}</pre>
      <div class="workbench-actions"><a href="${safeUrl(demo.manifestUrl)}" target="_blank" rel="noopener noreferrer">View manifest ↗</a><a href="${escapeHtml(demo.controlUrl)}" download>Download control ↓</a><button type="button" class="copy-command">Copy replay command</button></div>
      <div class="workbench-command"><span>$</span> ${escapeHtml(demo.command)}</div>
    </div>`;
  $("#demo-panel .copy-command").addEventListener("click", (event) => copyText(demo.command, event.currentTarget));
}
function initDemo() {
  $("#demo-tabs").innerHTML = catalog.demos.map((demo, index) => `<button type="button" role="tab" id="demo-tab-${index}" aria-controls="demo-panel" aria-selected="false">${escapeHtml(formatLabel(demo.format))}</button>`).join("");
  $("#demo-tabs").addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (button) renderDemo([...button.parentNode.children].indexOf(button));
  });
  $("#demo-tabs").addEventListener("keydown", (event) => {
    if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
    event.preventDefault();
    const tabs = [...$("#demo-tabs").children];
    let index = tabs.indexOf(document.activeElement);
    if (event.key === "Home") index = 0;
    else if (event.key === "End") index = tabs.length - 1;
    else index = (index + (event.key === "ArrowRight" ? 1 : -1) + tabs.length) % tabs.length;
    tabs[index].focus(); renderDemo(index);
  });
  renderDemo(0);
}
async function start() {
  try {
    const response = await fetch("catalog.json");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    catalog = await response.json();
    $("#stat-verified").textContent = catalog.summary.verified.toLocaleString();
    $("#stat-formats").textContent = catalog.summary.formats;
    $("#stat-ecosystems").textContent = catalog.summary.ecosystems;
    $("#stat-runnable").textContent = catalog.summary.runnable;
    renderFormats(); initAtlas(); initDemo(); renderMatrix();
    document.querySelectorAll("[data-copy]").forEach((button) => button.addEventListener("click", () => copyText(button.dataset.copy, button)));
  } catch (error) {
    $("#format-grid").innerHTML = '<p>The catalog could not be loaded. Build the site with <code>python3 website/build.py</code> and serve <code>website/dist</code>.</p>';
    $("#result-count").textContent = "Catalog unavailable.";
    console.error(error);
  }
}
start();
