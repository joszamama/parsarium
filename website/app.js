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
  png: '<rect x="54" y="16" width="88" height="70" rx="4" fill="#f8f9ff" stroke="#171448" stroke-width="2"/><rect x="63" y="25" width="70" height="52" fill="#f5efdf"/><rect x="63" y="25" width="35" height="26" fill="#fa7454"/><rect x="98" y="51" width="35" height="26" fill="#b9db79"/><circle cx="113" cy="36" r="10" fill="#171448"/><path d="M63 77 83 52l18 25" fill="none" stroke="#171448" stroke-width="3"/>',
  zip: '<rect x="55" y="19" width="87" height="68" rx="5" fill="#fff6e5" stroke="#171448" stroke-width="2"/><path d="M55 41h87M55 64h87" stroke="#171448" stroke-width="2"/><path d="M88 19v68" stroke="#171448" stroke-width="2" stroke-dasharray="5 4"/><rect x="79" y="45" width="18" height="15" rx="2" fill="#ff6877" stroke="#171448" stroke-width="2"/>',
  mp4: '<rect x="48" y="19" width="100" height="68" rx="5" fill="#171448"/><rect x="58" y="30" width="80" height="46" rx="2" fill="#f7e7be"/><path d="m94 39 20 14-20 14Z" fill="#ff6877"/><path d="M61 19v10m17-10v10m17-10v10m17-10v10m17-10v10" stroke="#f7e7be" stroke-width="4"/>',
  wav: '<path d="M40 52h15m4-16v32m9-43v54m9-36v18m9-40v62m9-46v28m9-34v40m9-22v8m9-30v50m9-38v26m9-17h16" fill="none" stroke="#171448" stroke-width="4" stroke-linecap="round"/><circle cx="98" cy="52" r="47" fill="none" stroke="#171448" stroke-width="2" stroke-dasharray="3 5"/>',
  pdf: '<path d="M62 14h59l17 18v58H62Z" fill="#fff8ed" stroke="#171448" stroke-width="2"/><path d="M121 14v18h17" fill="#f5ceb5" stroke="#171448" stroke-width="2"/><path d="M72 47h56M72 56h47M72 65h54M72 74h27" stroke="#171448" stroke-width="3"/><rect x="75" y="22" width="23" height="13" fill="#ff6877"/>',
  svg: '<circle cx="98" cy="52" r="39" fill="#fff7e4" stroke="#171448" stroke-width="2"/><path d="M62 70q28-56 68 0" fill="none" stroke="#ff6877" stroke-width="5"/><circle cx="62" cy="70" r="6" fill="#171448"/><circle cx="98" cy="27" r="6" fill="#171448"/><circle cx="130" cy="70" r="6" fill="#171448"/>',
  http11: '<rect x="47" y="19" width="103" height="69" rx="4" fill="#fff8ed" stroke="#171448" stroke-width="2"/><path d="M47 34h103" stroke="#171448" stroke-width="2"/><circle cx="57" cy="27" r="3" fill="#ff6877"/><circle cx="67" cy="27" r="3" fill="#e3c560"/><circle cx="77" cy="27" r="3" fill="#9ac466"/><path d="M59 47h30m-30 11h73M59 69h56" stroke="#171448" stroke-width="3"/><rect x="102" y="42" width="29" height="11" fill="#b7da81"/>',
  ascii_ply: '<path d="m96 15 45 70H51Z" fill="#f7ead0" stroke="#171448" stroke-width="2"/><path d="m96 15 6 42-51 28m51-28 39 28" fill="none" stroke="#171448" stroke-width="2"/><circle cx="96" cy="15" r="5" fill="#ff6877"/><circle cx="102" cy="57" r="5" fill="#ff6877"/><circle cx="51" cy="85" r="5" fill="#ff6877"/><circle cx="141" cy="85" r="5" fill="#ff6877"/>',
  ascii_pnm: '<rect x="54" y="17" width="92" height="72" fill="#fff8ea" stroke="#171448" stroke-width="2"/><path d="M77 17v72m23-72v72m23-72v72M54 41h92M54 65h92" stroke="#171448" stroke-width="2"/><rect x="55" y="18" width="21" height="22" fill="#ff6877"/><rect x="101" y="42" width="21" height="22" fill="#ffe05c"/><rect x="124" y="66" width="21" height="22" fill="#62d9e8"/>',
  mp3_id3v2: '<circle cx="98" cy="52" r="42" fill="#171448"/><circle cx="98" cy="52" r="27" fill="none" stroke="#6f846f" stroke-width="2"/><circle cx="98" cy="52" r="13" fill="#ff6877"/><circle cx="98" cy="52" r="4" fill="#f8f9ff"/><path d="m130 17 17 20" stroke="#171448" stroke-width="5" stroke-linecap="round"/><circle cx="147" cy="38" r="5" fill="#171448"/>'
};
const artColors = {
  png:"#f9d7b8", zip:"#c7d9f0", mp4:"#e4ccf0", wav:"#d5ebaa", pdf:"#ffd5c4",
  svg:"#bfe3dd", http11:"#e8dfa4", ascii_ply:"#e8cdb3", ascii_pnm:"#d6e2ff", mp3_id3v2:"#e9d0d8"
};

let catalog;
const pageSize = 18;
let visible = pageSize;
let activeDemoIndex = 0;
let activeDemo = null;
let activeTargetId = null;
let labStep = 0;
let labTimer = null;
const reducedMotion = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
function formatLabel(id) { return catalog.formats.find((format) => format.id === id)?.label ?? id; }
function roundRobin(items, groupKey, keyOrder) {
  const groups = new Map();
  for (const item of items) {
    const key = groupKey(item);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(item);
  }
  const queues = keyOrder
    ? [...keyOrder.map((key) => groups.get(key)).filter(Boolean),
       ...[...groups].filter(([key]) => !keyOrder.includes(key)).map(([, group]) => group)]
    : [...groups.values()];
  const ordered = [];
  let remaining = items.length;
  while (remaining) for (const group of queues) {
    if (group.length) { ordered.push(group.shift()); remaining -= 1; }
  }
  return ordered;
}
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
      <span class="format-content"><span class="format-category">${escapeHtml(format.category)}</span><span class="format-name">${escapeHtml(format.label)}</span><span class="format-count"><b>${format.verified}</b> third-party paths · <b>${format.runnable}</b> runnable targets</span></span>
    </button>`).join("");
  $("#format-grid").addEventListener("click", (event) => {
    const button = event.target.closest("[data-format]");
    if (!button) return;
    $("#format-filter").value = button.dataset.format;
    $("#ecosystem-filter").value = "";
    $("#search").value = "";
    visible = pageSize;
    renderAtlas();
    showDemoForFormat(button.dataset.format);
    $("#atlas").scrollIntoView({ behavior: reducedMotion() ? "instant" : "smooth" });
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
  if (activeTargetId) params.set("target", activeTargetId);
  const url = `${location.pathname}${params.size ? `?${params}` : ""}${activeTargetId ? "#specimen" : location.hash}`;
  history.replaceState(null, "", url);
}
function parserCard(parser) {
  const project = parser.projectUrl ? `<a href="${safeUrl(parser.projectUrl)}" target="_blank" rel="noopener noreferrer">Harness ↗</a>` : "";
  const badge = parser.type === "standard" ? "STANDARD + RUNNABLE" : parser.projectUrl ? "RUNNABLE" : "";
  const details = parser.type === "standard" ? "standard library API" : `${parser.license} · scope: ${parser.scope}`;
  const popularity = parser.type === "standard"
    ? "Standard/runtime API · outside third-party ranking"
    : parser.rank?.match(/^\d+=?$/)
      ? `#${escapeHtml(parser.rank.replace("=", ""))}${parser.rank.endsWith("=") ? " (tie)" : ""} within ${escapeHtml(ecoLabel[parser.ecosystem])} × ${escapeHtml(formatLabel(parser.format))} · ${escapeHtml(parser.popularityMetric)}: ${escapeHtml(parser.metricValue)}`
      : parser.rank === "unranked" ? "Unranked · adoption metric unavailable" : "Ranking match unresolved · see source";
  return `<article class="parser-card-item">
    <div class="parser-meta"><span>${escapeHtml(formatLabel(parser.format))} / ${escapeHtml(ecoLabel[parser.ecosystem])}</span>${badge ? `<span class="runnable-badge">${badge}</span>` : ""}</div>
    <h3>${escapeHtml(parser.name)}</h3><span class="parser-version">${escapeHtml(parser.version)} · ${escapeHtml(details)}</span>
    <p class="parser-popularity">${popularity}${parser.rankingUrl ? ` <a href="${safeUrl(parser.rankingUrl)}" target="_blank" rel="noopener noreferrer">Ranking ↗</a>` : ""}</p>
    <p class="parser-api"><strong>Input API:</strong> ${escapeHtml(parser.inputApi)}</p>
    <p class="parser-family">Family: ${escapeHtml(parser.family)}</p>
    <div class="parser-card-links"><a href="${safeUrl(parser.guideUrl)}" target="_blank" rel="noopener noreferrer">Parser guide ↗</a><a href="${safeUrl(parser.documentation)}" target="_blank" rel="noopener noreferrer">API docs ↗</a><a href="${safeUrl(parser.evidenceUrl)}" target="_blank" rel="noopener noreferrer">Evidence ↗</a>${project}</div>
    ${parser.targetId ? `<button class="use-target" type="button" data-use-target="${escapeHtml(parser.targetId)}">Use this target <span aria-hidden="true">→</span></button>` : ""}
  </article>`;
}
function renderAtlas() {
  const filters = currentFilters();
  const pool = filters.runnable
    ? catalog.parsers.filter((parser) => parser.projectUrl).concat(catalog.standardTargets)
    : catalog.parsers;
  let result = pool.filter((parser) => {
    if (filters.format && parser.format !== filters.format) return false;
    if (filters.ecosystem && parser.ecosystem !== filters.ecosystem) return false;
    if (filters.query) {
      const haystack = [parser.name, parser.inputApi, parser.family, parser.scope, parser.version].join(" ").toLocaleLowerCase();
      if (!haystack.includes(filters.query)) return false;
    }
    return true;
  });
  if (!filters.format) {
    const cellOrder = [];
    for (let offset = 0; offset < catalog.ecosystems.length; offset += 1) {
      catalog.formats.forEach((format, index) => cellOrder.push(
        `${format.id}/${catalog.ecosystems[(index + offset) % catalog.ecosystems.length]}`
      ));
    }
    result = roundRobin(result, (parser) => `${parser.format}/${parser.ecosystem}`, cellOrder);
  }
  else if (!filters.ecosystem) result = roundRobin(result, (parser) => parser.ecosystem);
  const shown = result.slice(0, visible);
  const view = !filters.format ? " · across formats and ecosystems" : !filters.ecosystem ? " · across ecosystems" : "";
  $("#result-count").textContent = `Showing ${shown.length.toLocaleString()} of ${result.length.toLocaleString()} ${filters.runnable ? "runnable targets" : "verified package paths"}${view}`;
  $("#parser-grid").innerHTML = shown.length ? shown.map(parserCard).join("") : '<div class="empty-state">No parsers match those filters. Try another format, ecosystem, or search term.</div>';
  $("#load-more").hidden = shown.length >= result.length;
  const note = $("#cell-note");
  if (filters.format && filters.ecosystem) {
    const cell = catalog.cells.find((item) => item.format === filters.format && item.ecosystem === filters.ecosystem);
    note.hidden = false;
    note.innerHTML = `<strong>${escapeHtml(formatLabel(filters.format))} × ${escapeHtml(ecoLabel[filters.ecosystem])}</strong>
      <p>${cell.verified} verified third-party paths · ${cell.runnable} runnable harness${cell.runnable === 1 ? "" : "es"} · ${cell.standard} standard/runtime APIs · ${cell.unresolved} unresolved documentation leads.</p>
      <div class="cell-links"><a href="${safeUrl(cell.cellGuideUrl)}" target="_blank" rel="noopener noreferrer">All parser & runtime guides ↗</a>
      <a href="${safeUrl(cell.rankingUrl)}" target="_blank" rel="noopener noreferrer">Popularity ranking & search limits ↗</a>
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
  ["format-filter", "ecosystem-filter", "runnable-filter"].forEach((id) => $(`#${id}`).addEventListener("change", () => {
    visible = pageSize;
    renderAtlas();
    if (id === "format-filter" && $("#format-filter").value) showDemoForFormat($("#format-filter").value);
  }));
  $("#search").addEventListener("input", () => { visible = pageSize; renderAtlas(); });
  $("#clear-filters").addEventListener("click", () => {
    $("#format-filter").value = ""; $("#ecosystem-filter").value = ""; $("#search").value = ""; $("#runnable-filter").checked = false;
    visible = pageSize; renderAtlas(); renderDemo(0);
  });
  $("#load-more").addEventListener("click", () => { visible += pageSize; renderAtlas(); });
  $("#parser-grid").addEventListener("click", (event) => {
    const button = event.target.closest("[data-use-target]");
    if (!button) return;
    renderTarget(button.dataset.useTarget);
    $("#specimen").scrollIntoView({ behavior: reducedMotion() ? "instant" : "smooth" });
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "/" && !["INPUT", "TEXTAREA", "SELECT"].includes(document.activeElement.tagName)) {
      event.preventDefault(); $("#search").focus(); $("#atlas").scrollIntoView({ behavior: reducedMotion() ? "instant" : "smooth" });
    }
  });
  renderAtlas();
}
function showDemoForFormat(format) {
  const index = catalog.demos.findIndex((demo) => demo.format === format);
  if (index >= 0) renderDemo(index);
}
function commandBlock(label, command, key) {
  return `<div class="command-block"><div class="command-label"><span>${escapeHtml(label)}</span><button type="button" data-command="${key}">Copy</button></div><pre><code><span>$</span> ${escapeHtml(command)}</code></pre></div>`;
}
function renderDemo(index) {
  const demo = catalog.demos[index];
  activeDemoIndex = index;
  activeTargetId = null;
  renderWorkbench(demo, false);
}
function renderTarget(targetId) {
  const demo = catalog.targets[targetId];
  if (!demo) return;
  activeDemoIndex = catalog.demos.findIndex((item) => item.format === demo.format);
  activeTargetId = targetId;
  renderWorkbench(demo, true);
}
function renderWorkbench(demo, selectedTarget) {
  activeDemo = demo;
  labStep = 0;
  stopLab();
  const format = catalog.formats.find((item) => item.id === demo.format);
  $("#format-guide").href = safeUrl(format.guideUrl);
  $("#format-guide").textContent = `Read the ${format.label} format guide ↗`;
  $("#demo-tabs").querySelectorAll("button").forEach((button, buttonIndex) => {
    button.setAttribute("aria-selected", String(buttonIndex === activeDemoIndex));
    button.tabIndex = buttonIndex === activeDemoIndex ? 0 : -1;
  });
  const panel = $("#demo-panel");
  panel.setAttribute("aria-labelledby", `demo-tab-${activeDemoIndex}`);
  const controlName = demo.control.split("/").pop();
  const afl = demo.aflCommands.map((command) => `<span>$</span> ${escapeHtml(command)}`).join("\n");
  const controlLink = selectedTarget
    ? `<a href="${safeUrl(demo.controlUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(controlName)} ↗</a>`
    : `<a href="${escapeHtml(demo.controlUrl)}" download>${escapeHtml(controlName)} ↓</a>`;
  const resultPreview = Object.fromEntries(Object.entries(demo.expectedOutput ?? {}).slice(0, 4));
  const coverageBadge = demo.coverageKind === "native_binary_edges"
    ? `${Number(demo.coverageTuples || 0).toLocaleString()} binary edge tuples · no source lines`
    : Number.isInteger(demo.coverageLines)
      ? `${demo.coverageLines.toLocaleString()} package-source lines covered`
      : "See guide for coverage scope";
  panel.innerHTML = `<div class="workbench-top"><span>${escapeHtml(formatLabel(demo.format))} / ${selectedTarget ? "YOUR SELECTED TARGET" : "FEATURED EXAMPLE"}</span><span class="workbench-lights" aria-hidden="true"><i></i><i></i><i></i></span></div>
    <div class="workbench-body">
      ${selectedTarget ? `<div class="selected-target-note"><span>Picked from the atlas</span><button type="button" id="restore-example">Show featured example ↺</button></div>` : ""}
      <div class="target-head"><div><span class="workbench-step">PINNED PARSER</span><h3>${escapeHtml(demo.package)}</h3><p>${escapeHtml(ecoLabel[demo.ecosystem])} · release ${escapeHtml(demo.release)}</p></div><a href="${safeUrl(demo.projectGuideUrl)}" target="_blank" rel="noopener noreferrer">Harness guide ↗</a></div>
      <p class="target-api"><strong>Documented input API</strong><code>${escapeHtml(demo.inputApi)}</code></p>
      <div class="result-preview"><div class="result-preview-head"><strong>Observed control result</strong><span>${escapeHtml(coverageBadge)}</span></div><pre>${escapeHtml(JSON.stringify(resultPreview))}</pre></div>
      <div class="run-step"><div class="run-step-head"><h4>Check the target</h4></div><p>Run its supplied valid control, ${controlLink} (${demo.bytes.toLocaleString()} bytes).</p>
        ${commandBlock("VALID CONTROL", demo.controlCommand, "control")}
        <details class="control-evidence"><summary>What does this control check?</summary><p>These fields were observed during format-aware control verification and checked against the harness receipt. This command runs the same control through the Docker harness and saves a JSON receipt.</p><pre class="output-view">${escapeHtml(JSON.stringify(demo.expectedOutput, null, 2))}</pre>${demo.coverageLimit ? `<p class="coverage-limit">Coverage scope: ${escapeHtml(demo.coverageLimit)}</p>` : ""}</details>
      </div>
      <div class="run-step"><div class="run-step-head"><h4>Run your file</h4></div><p>Replace <code>INPUT_FILE</code> with a local file of the same format.</p>
        ${commandBlock("ONE INPUT", demo.inputCommand, "input")}
      </div>
      <div class="run-step"><div class="run-step-head"><h4>Replay a corpus</h4></div><p>Replace <code>CORPUS_DIR</code> with a directory of files from Fandango, another generator, or your own collection. Parsarium records each run.</p>
        ${commandBlock("MANY INPUTS", demo.replayCommand, "replay")}
        <details class="afl-details"><summary>Use AFL++ with this target</summary><p>Build the instrumented image, prepare its valid seed, then run a short campaign.</p><pre><code>${afl}</code></pre><button type="button" data-command="afl">Copy AFL++ commands</button></details>
      </div>
    </div>`;
  panel.querySelectorAll("[data-command]").forEach((button) => button.addEventListener("click", () => {
    const key = button.dataset.command;
    const command = key === "afl" ? demo.aflCommands.join("\n") : demo[`${key}Command`];
    copyText(command, button);
  }));
  panel.querySelector("#restore-example")?.addEventListener("click", () => renderDemo(activeDemoIndex));
  updateUrl(currentFilters());
  renderLab();
}
function stopLab() {
  if (labTimer !== null) clearInterval(labTimer);
  labTimer = null;
  const button = $("#lab-play");
  if (button) { button.hidden = reducedMotion(); button.innerHTML = 'Play walkthrough <span aria-hidden="true">▶</span>'; }
}
function renderLab() {
  const demo = activeDemo;
  const format = formatLabel(demo.format);
  const control = demo.control.split("/").pop();
  const formatClues = {
    png: "PNG readers interpret named chunks such as IHDR and IDAT before they can report dimensions or pixels.",
    zip: "ZIP readers use archive records and the central directory to identify and open entries.",
    mp4: "MP4 readers walk nested boxes to find tracks, timing, and media metadata.",
    wav: "WAV readers interpret RIFF chunks, including the format and sample-data chunks.",
    pdf: "PDF readers resolve document objects and pages before returning page-level information.",
    svg: "SVG readers interpret XML elements and attributes as vector graphics.",
    http11: "HTTP/1.1 parsers separate the start line, headers, and message body from the byte stream.",
    ascii_ply: "ASCII PLY readers use the header to define the vertex and face records that follow.",
    ascii_pnm: "ASCII PNM readers use the magic number, dimensions, and sample values to build an image.",
    mp3_id3v2: "MP3 with ID3v2 readers interpret tag headers and frames before exposing audio metadata."
  };
  const coverageObservation = demo.coverageKind === "native_binary_edges"
    ? `The control produced format-specific fields and recorded <strong>${Number(demo.coverageTuples || 0).toLocaleString()} AFL++ edge tuples</strong> inside a pinned native parser module. This is binary feedback, not source-line coverage. See the harness guide for the measured scope.`
    : Number.isInteger(demo.coverageLines)
      ? `The control produced format-specific fields and covered <strong>${demo.coverageLines.toLocaleString()} package-source lines</strong>. See the harness guide for what was instrumented; this control does not establish support for every variant.`
      : `The control produced format-specific fields. See the harness guide for its coverage receipt and measurement limits.`;
  const steps = [
    {title: "A file the parser understands", tag: "CONTROL FILE", body: `The small valid control <strong>${escapeHtml(control)}</strong> (${demo.bytes.toLocaleString()} bytes) establishes a baseline for this ${format} target. Generators such as Fandango can supply further files when a matching format spec is available.`, detail: activeTargetId ? `<a href="${safeUrl(demo.controlUrl)}" target="_blank" rel="noopener noreferrer">Open this control ↗</a>` : `<a href="${escapeHtml(demo.controlUrl)}" download>Download this control ↓</a>`},
    {title: "A specific input API", tag: "PARSER ENTRY", body: `Pinned release <strong>${escapeHtml(demo.package)} ${escapeHtml(demo.release)}</strong> receives the file through the documented API below. ${formatClues[demo.format]}`, detail: `<code>${escapeHtml(demo.inputApi)}</code>`},
    {title: "An observable result", tag: "COVERAGE RECEIPT", body: coverageObservation, detail: `<pre>${escapeHtml(JSON.stringify(demo.expectedOutput, null, 2))}</pre>`},
    {title: "A repeatable experiment", tag: "CORPUS REPLAY", body: `Replay a directory of ${format} files through this target. Receipts keep input hashes and per-input outcomes. AFL++ uses parser feedback to explore further inputs. The parser's reported result matters more than a successful harness exit.`, detail: `<code>${escapeHtml(demo.replayCommand)}</code>`}
  ];
  const current = steps[labStep];
  $("#lab-context").textContent = `${format} · ${demo.package} · ${demo.ecosystem.toUpperCase()} ${activeTargetId ? "selected target" : "example"}`;
  $("#lab-stage").dataset.step = String(labStep);
  $("#lab-stage").querySelectorAll("[data-lab-step]").forEach((button) => button.setAttribute("aria-pressed", String(Number(button.dataset.labStep) === labStep)));
  $("#lab-panel").innerHTML = `<div class="lab-tag">${current.tag}</div><h3>${current.title}</h3><p>${current.body}</p><div class="lab-detail">${current.detail}</div>`;
  $("#lab-next").disabled = labStep === steps.length - 1;
}
function initLab() {
  $("#lab-play").hidden = reducedMotion();
  $("#lab-stage").addEventListener("click", (event) => {
    const button = event.target.closest("[data-lab-step]");
    if (!button) return;
    stopLab();
    labStep = Number(button.dataset.labStep);
    renderLab();
  });
  $("#lab-next").addEventListener("click", () => { stopLab(); labStep = Math.min(labStep + 1, 3); renderLab(); });
  $("#lab-play").addEventListener("click", () => {
    if (reducedMotion()) return;
    if (labTimer !== null) { stopLab(); return; }
    labStep = 0;
    renderLab();
    $("#lab-play").innerHTML = 'Pause walkthrough <span aria-hidden="true">Ⅱ</span>';
    labTimer = setInterval(() => {
      if (labStep === 3) { stopLab(); return; }
      labStep += 1;
      renderLab();
    }, 1700);
  });
  renderLab();
}
function initDemo() {
  $("#demo-tabs").innerHTML = catalog.demos.map((demo, index) => `<button type="button" role="tab" id="demo-tab-${index}" aria-controls="demo-panel" aria-selected="false">${escapeHtml(formatLabel(demo.format))}</button>`).join("");
  $("#demo-tabs").addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (button) {
      const index = [...button.parentNode.children].indexOf(button);
      renderDemo(index);
      $("#format-filter").value = catalog.demos[index].format;
      visible = pageSize;
      renderAtlas();
    }
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
    $("#format-filter").value = catalog.demos[index].format;
    visible = pageSize;
    renderAtlas();
  });
  showDemoForFormat($("#format-filter").value || catalog.demos[0].format);
}
function initMobileMenu() {
  const toggle = $("#mobile-menu-toggle");
  const menu = $("#mobile-nav");
  const close = () => { menu.hidden = true; toggle.setAttribute("aria-expanded", "false"); };
  toggle.addEventListener("click", () => {
    const open = menu.hidden;
    menu.hidden = !open;
    toggle.setAttribute("aria-expanded", String(open));
  });
  menu.addEventListener("click", (event) => { if (event.target.closest("a")) close(); });
  document.addEventListener("keydown", (event) => { if (event.key === "Escape") close(); });
  matchMedia("(min-width: 801px)").addEventListener("change", (event) => { if (event.matches) close(); });
}
async function start() {
  try {
    const requestedTarget = new URLSearchParams(location.search).get("target");
    const embedded = $("#catalog-data");
    if (embedded) {
      catalog = JSON.parse(embedded.textContent);
    } else {
      const response = await fetch("catalog.json", { cache: "no-store" });
      if (!response.ok) throw new Error(`Catalog HTTP ${response.status}`);
      catalog = await response.json();
    }
    $("#stat-verified").textContent = catalog.summary.verified.toLocaleString();
    $("#stat-formats").textContent = catalog.summary.formats;
    $("#stat-ecosystems").textContent = catalog.summary.ecosystems;
    $("#stat-runnable").textContent = catalog.summary.runnable;
    renderFormats(); initAtlas(); initDemo(); initLab(); initMobileMenu();
    if (requestedTarget && catalog.targets[requestedTarget]) renderTarget(requestedTarget);
    document.querySelectorAll("[data-copy]").forEach((button) => button.addEventListener("click", () => copyText(button.dataset.copy, button)));
    if (["#formats", "#atlas", "#specimen", "#lab"].includes(location.hash)) {
      requestAnimationFrame(() => $(location.hash).scrollIntoView({ behavior: "instant" }));
    }
  } catch (error) {
    $("#format-grid").innerHTML = '<p>The catalog view could not start. <a href="">Reload the page</a> or open the <a href="catalog.json">catalog data</a>.</p>';
    $("#result-count").textContent = "Catalog view unavailable.";
    console.error(error);
  }
}
start();
