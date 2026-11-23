(async () => {
  const root = document.querySelector("#bench");
  if (!root) return;
  const es = document.body.dataset.lang === "es";
  const T = es ? {
    loading: "Cargando el catálogo…", targets: "targets", formats: "formatos", ecosystems: "lenguajes",
    families: "familias", id: "ID", none: "Ningún target coincide con esta selección.",
    cols: ["Formato", "Lenguaje", "Paquete", "Familia", "API de entrada", "Rango", "Feedback AFL++"],
    showAll: (n) => `Mostrar los ${n} targets`, std: "estándar", harness: "harness",
    modes: { control: "Controles", file: "Mis archivos", replay: "Corpus", afl: "AFL++", fandango: "Fandango" },
    unranked: "—",
  } : {
    loading: "Loading the catalog…", targets: "targets", formats: "formats", ecosystems: "languages",
    families: "families", id: "ID", none: "No target matches this selection.",
    cols: ["Format", "Language", "Package", "Family", "Input API", "Rank", "AFL++ feedback"],
    showAll: (n) => `Show all ${n} targets`, std: "standard", harness: "harness",
    modes: { control: "Controls", file: "My files", replay: "Corpus", afl: "AFL++", fandango: "Fandango" },
    unranked: "—",
  };
  const ECO = { c: "C", cpp: "C++", go: "Go", java: "Java", javascript: "JavaScript", python: "Python", rust: "Rust", php: "PHP" };
  const summaryEl = root.querySelector(".sel-summary");
  summaryEl.textContent = T.loading;

  const catalog = await fetch(root.dataset.catalog).then((r) => r.json());
  const formats = catalog.formats.map((f) => f.id);
  const ecosystems = catalog.ecosystems;
  const label = Object.fromEntries(catalog.formats.map((f) => [f.id, f.label]));
  const all = Object.entries(catalog.targets).map(([id, t]) => ({ id, ...t }));
  const bridge = /^(go|java|javascript|python|php)_parser_source/;
  const rankOf = (t) => {
    const n = parseInt(String(t.rank || "").replace("=", ""), 10);
    return Number.isFinite(n) ? n : (t.type === "standard" ? 5000 : 10000);
  };
  const feedbackLabel = (t) => {
    if (!t.aflFeedback) return "—";
    if (bridge.test(t.aflFeedback)) return `${t.aflFeedback.split("_")[0]} bridge`;
    return "compiled edges";
  };

  // ---- state <-> URL
  const params = new URLSearchParams(location.search);
  const listParam = (key, universe, fallback) => {
    const raw = params.get(key);
    if (!raw) return new Set(fallback);
    const picked = raw.split(",").filter((v) => universe.includes(v));
    return new Set(picked.length ? picked : fallback);
  };
  const state = {
    f: listParam("f", formats, params.get("format") ? [params.get("format")] : ["png"]),
    e: listParam("e", ecosystems, ecosystems),
    n: ["1", "3", "5", "10", "all"].includes(params.get("n")) ? params.get("n") : "all",
    family: params.get("family") === "1",
    std: params.get("std") !== "0",
    native: params.get("native") === "1",
    mode: ["control", "file", "replay", "afl", "fandango"].includes(params.get("mode")) ? params.get("mode") : "control",
    tab: params.get("tab") || "targets",
    expanded: false,
  };
  const query = () => {
    const q = new URLSearchParams();
    q.set("f", [...state.f].join(","));
    if (state.e.size !== ecosystems.length) q.set("e", [...state.e].join(","));
    if (state.n !== "all") q.set("n", state.n);
    if (state.family) q.set("family", "1");
    if (!state.std) q.set("std", "0");
    if (state.native) q.set("native", "1");
    if (state.mode !== "control") q.set("mode", state.mode);
    if (state.tab !== "targets") q.set("tab", state.tab);
    return q.toString();
  };
  const canonicalQuery = () => {
    const q = new URLSearchParams(query());
    q.delete("tab"); q.delete("mode");
    return q.toString();
  };

  // ---- selection
  const select = () => {
    let pool = all.filter((t) => state.f.has(t.format) && state.e.has(t.ecosystem)
      && (state.std || t.type !== "standard")
      && (!state.native || (t.aflFeedback && !bridge.test(t.aflFeedback))));
    pool.sort((a, b) => formats.indexOf(a.format) - formats.indexOf(b.format)
      || ecosystems.indexOf(a.ecosystem) - ecosystems.indexOf(b.ecosystem)
      || rankOf(a) - rankOf(b) || a.package.localeCompare(b.package));
    if (state.family) {
      const best = new Map();
      for (const t of [...pool].sort((a, b) => rankOf(a) - rankOf(b))) {
        const key = `${t.format}|${t.family}`;
        if (!best.has(key)) best.set(key, t.id);
      }
      const keep = new Set(best.values());
      pool = pool.filter((t) => keep.has(t.id));
    }
    if (state.n !== "all") {
      const limit = Number(state.n);
      const seen = new Map();
      pool = pool.filter((t) => {
        const key = `${t.format}|${t.ecosystem}`;
        seen.set(key, (seen.get(key) || 0) + 1);
        return seen.get(key) <= limit;
      });
    }
    return pool;
  };
  const hashId = async (ids) => {
    const text = [...ids].sort().join("\n");
    if (crypto.subtle) {
      const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
      return "sel-" + [...new Uint8Array(digest)].slice(0, 5).map((b) => b.toString(16).padStart(2, "0")).join("");
    }
    let h = 2166136261;
    for (let i = 0; i < text.length; i++) { h ^= text.charCodeAt(i); h = Math.imul(h, 16777619); }
    return "sel-" + (h >>> 0).toString(16).padStart(10, "0");
  };

  // ---- controls
  const chipGroup = (key, values, text) => {
    const box = root.querySelector(`.chips[data-group="${key}"]`);
    box.innerHTML = values.map((v) => `<button type="button" class="chip" data-v="${v}">${text(v)}</button>`).join("");
    box.addEventListener("click", (event) => {
      const b = event.target.closest("button"); if (!b) return;
      const set = state[key];
      if (set.has(b.dataset.v) && set.size > 1) set.delete(b.dataset.v); else set.add(b.dataset.v);
      update();
    });
  };
  chipGroup("f", formats, (v) => label[v]);
  chipGroup("e", ecosystems, (v) => ECO[v]);
  root.querySelectorAll("[data-all]").forEach((b) => b.addEventListener("click", () => {
    const key = b.dataset.all;
    const universe = key === "f" ? formats : ecosystems;
    state[key] = state[key].size === universe.length ? new Set([universe[0]]) : new Set(universe);
    update();
  }));
  root.querySelector('.seg[data-group="n"]').addEventListener("click", (event) => {
    const b = event.target.closest("button"); if (!b) return;
    state.n = b.dataset.v; update();
  });
  root.querySelectorAll("[data-opt]").forEach((input) => input.addEventListener("change", () => {
    state[input.dataset.opt] = input.checked; update();
  }));
  const modeBox = root.querySelector('[data-group="mode"]');
  modeBox.innerHTML = Object.entries(T.modes).map(([k, v]) => `<button type="button" class="chip" data-v="${k}">${v}</button>`).join("");
  modeBox.addEventListener("click", (event) => {
    const b = event.target.closest("button"); if (!b) return;
    state.mode = b.dataset.v; update();
  });
  root.querySelectorAll('[role="tab"]').forEach((tab) => tab.addEventListener("click", () => {
    state.tab = tab.dataset.tab; update();
  }));

  // ---- outputs
  const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const pageUrl = () => `https://parsarium.com/${es ? "es/" : ""}bench/?${canonicalQuery()}`;

  const scriptFor = (id, picked) => {
    const fmts = [...new Set(picked.map((t) => t.format))];
    const single = fmts.length === 1;
    const lines = [
      "#!/usr/bin/env bash",
      `# Parsarium ${id}: ${picked.length} targets, ${fmts.length} formats`,
      `# ${pageUrl()}`,
      `# Built from parsarium commit ${catalog.commit}. Install from source: see https://parsarium.com/manual/`,
      "set -uo pipefail",
      `OUT="\${OUT:-runs/${id}}"`,
    ];
    if (state.mode === "file") {
      lines.push(single
        ? 'INPUT="${1:?usage: run-selection.sh FILE}"'
        : 'INPUTS="${1:?usage: run-selection.sh DIR  (one subdirectory per format, e.g. DIR/png/)}"');
    } else if (state.mode === "replay") {
      lines.push(single
        ? 'CORPUS="${1:?usage: run-selection.sh CORPUS_DIR}"'
        : 'CORPUS="${1:?usage: run-selection.sh CORPUS_DIR  (one subdirectory per format, e.g. CORPUS_DIR/png/)}"');
    } else if (state.mode === "afl") {
      lines.push('SECONDS_PER_TARGET="${SECONDS_PER_TARGET:-3600}"', 'COUNT="${COUNT:-100}"', 'SEED="${SEED:-42}"', "parsarium fandango setup || exit 1");
    } else if (state.mode === "fandango") {
      lines.push('COUNT="${COUNT:-100}"', 'SEED="${SEED:-42}"', "parsarium fandango setup || exit 1");
    }
    lines.push('PARSARIUM="${PARSARIUM:-$(parsarium home --path)}"', 'mkdir -p "$OUT"', "", "TARGETS=(");
    for (const t of picked) lines.push(`  "${t.format} ${t.ecosystem} ${t.slug} ${t.control}"`);
    lines.push(")", "", 'for entry in "${TARGETS[@]}"; do', '  read -r fmt eco slug control <<<"$entry"', '  name="$fmt-$eco-$slug"', '  echo "== $name"');
    const fail = '|| echo "$name" >> "$OUT/failed.txt"';
    if (state.mode === "control") {
      lines.push(`  parsarium run "$fmt" "$eco" "$slug" "$PARSARIUM/$control" --results "$OUT/$name" ${fail}`);
    } else if (state.mode === "file") {
      if (single) lines.push(`  parsarium run "$fmt" "$eco" "$slug" "$INPUT" --results "$OUT/$name" ${fail}`);
      else lines.push('  for input in "$INPUTS/$fmt"/*; do', '    [ -f "$input" ] || continue',
        `    parsarium run "$fmt" "$eco" "$slug" "$input" --results "$OUT/$name/$(basename "$input")" ${fail}`, "  done");
    } else if (state.mode === "replay") {
      const dir = single ? '"$CORPUS"' : '"$CORPUS/$fmt"';
      lines.push(`  parsarium replay "$fmt" "$eco" "$slug" ${dir} "$OUT/$name" ${fail}`);
    } else if (state.mode === "fandango") {
      lines.push(`  parsarium fandango generate "$fmt" "$eco" "$slug" "$OUT/$name" --count "$COUNT" --seed "$SEED" --replay ${fail}`);
    } else {
      lines.push('  parsarium afl build "$fmt" "$eco" "$slug" || { echo "$name" >> "$OUT/failed.txt"; continue; }',
        '  parsarium afl prepare "$fmt" "$eco" "$slug" "$OUT/$name" --fandango "$COUNT" --fandango-seed "$SEED" || { echo "$name" >> "$OUT/failed.txt"; continue; }',
        `  parsarium afl run "$OUT/$name" --seconds "$SECONDS_PER_TARGET" ${fail}`,
        '  parsarium afl summary "$OUT/$name" >/dev/null || true');
    }
    lines.push("done", 'echo "Receipts in $OUT"');
    return lines.join("\n") + "\n";
  };

  const manifestFor = (id, picked) => JSON.stringify({
    schema: "parsarium-selection/1",
    id,
    url: pageUrl(),
    commit: catalog.commit,
    created: new Date().toISOString().slice(0, 10),
    query: {
      formats: [...state.f], ecosystems: [...state.e], perCell: state.n,
      oneTargetPerFamily: state.family, standardApis: state.std, compiledFeedbackOnly: state.native,
    },
    counts: {
      targets: picked.length,
      formats: new Set(picked.map((t) => t.format)).size,
      ecosystems: new Set(picked.map((t) => t.ecosystem)).size,
      families: new Set(picked.map((t) => `${t.format}|${t.family}`)).size,
    },
    targets: picked.map((t) => ({
      id: t.id, format: t.format, ecosystem: t.ecosystem, package: t.package, release: t.release,
      type: t.type, family: t.family, inputApi: t.inputApi, control: t.control,
      aflFeedback: t.aflFeedback, verifiedAt: t.verifiedAt,
    })),
  }, null, 2) + "\n";

  const reportFor = (id, picked) => {
    const fam = new Set(picked.map((t) => `${t.format}|${t.family}`)).size;
    const fm = new Set(picked.map((t) => t.format)).size;
    const ec = new Set(picked.map((t) => t.ecosystem)).size;
    const rows = picked.map((t) => `| ${label[t.format]} | ${ECO[t.ecosystem]} | ${t.package} | ${t.release} | ${feedbackLabel(t)} |`);
    return es ? [
      "### Objetivos", "",
      `Usamos la selección de Parsarium \`${id}\` (commit \`${catalog.commit}\`): ${picked.length} parsers en ${fm} formatos y ${ec} lenguajes, de ${fam} familias de parsers distintas. Cada target tiene una versión fijada, una API de entrada documentada y un archivo de control válido.`,
      `Selección: ${pageUrl()}`, "",
      "| Formato | Lenguaje | Paquete | Versión | Feedback AFL++ |", "| --- | --- | --- | --- | --- |", ...rows, "",
      "### Configuración", "",
      `- Modo: ${T.modes[state.mode]}`, "- Presupuesto por target: …", "- Repeticiones: …", "- Máquina: …", "",
      "Los recuentos de feedback de AFL++ dependen de la instrumentación; los comparamos solo dentro de un mismo target.", "",
    ].join("\n") : [
      "### Targets", "",
      `We use Parsarium selection \`${id}\` (commit \`${catalog.commit}\`): ${picked.length} parsers across ${fm} formats and ${ec} languages, from ${fam} distinct parser families. Each target has a pinned release, a documented input API, and a valid control file.`,
      `Selection: ${pageUrl()}`, "",
      "| Format | Language | Package | Release | AFL++ feedback |", "| --- | --- | --- | --- | --- |", ...rows, "",
      "### Setup", "",
      `- Mode: ${T.modes[state.mode]}`, "- Budget per target: …", "- Repetitions: …", "- Machine: …", "",
      "AFL++ feedback counts depend on the instrumentation, so we compare them only within the same target.", "",
    ].join("\n");
  };

  const tableFor = (picked) => {
    if (!picked.length) return `<p class="panel-note">${T.none}</p>`;
    const limit = state.expanded ? picked.length : 150;
    const rows = picked.slice(0, limit).map((t) => `<tr>
      <td>${esc(label[t.format])}</td><td>${ECO[t.ecosystem]}</td>
      <td><a class="pkg" href="${esc(t.repository || t.registryUrl || t.projectGuideUrl)}" rel="noopener">${esc(t.package)}</a> <span class="rel">${esc(t.release)}${t.repository || t.registryUrl ? ` · <a href="${esc(t.projectGuideUrl)}" rel="noopener">${T.harness}</a>` : ""}</span>${t.type === "standard" ? ` <span class="tag std">${T.std}</span>` : ""}</td>
      <td>${esc(t.family)}</td>
      <td class="api" title="${esc(t.inputApi)}">${esc(t.inputApi)}</td>
      <td class="num">${esc(t.rank || T.unranked)}</td>
      <td>${feedbackLabel(t)}${t.aflEdges ? ` <span class="rel">${t.aflEdges}</span>` : ""}</td></tr>`).join("");
    const more = picked.length > limit ? `<p class="more"><button type="button" class="chip" data-more>${T.showAll(picked.length)}</button></p>` : "";
    return `<div class="table-scroll"><table class="t"><thead><tr>${T.cols.map((c) => `<th>${c}</th>`).join("")}</tr></thead><tbody>${rows}</tbody></table></div>${more}`;
  };

  const downloads = {};
  const setDownload = (key, name, text, type) => {
    if (downloads[key]) URL.revokeObjectURL(downloads[key]);
    downloads[key] = URL.createObjectURL(new Blob([text], { type }));
    const a = root.querySelector(`[data-download="${key}"]`);
    a.href = downloads[key]; a.download = name;
  };

  let ticket = 0;
  async function update() {
    const mine = ++ticket;
    history.replaceState(null, "", `?${query()}${location.hash}`);
    root.querySelectorAll(".chips[data-group] .chip").forEach((b) => {
      const key = b.parentElement.dataset.group;
      b.setAttribute("aria-pressed", String(state[key].has(b.dataset.v)));
    });
    root.querySelectorAll('.seg[data-group="n"] button').forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.v === state.n)));
    root.querySelectorAll("[data-opt]").forEach((input) => { input.checked = state[input.dataset.opt]; });
    modeBox.querySelectorAll(".chip").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.v === state.mode)));
    root.querySelectorAll('[role="tab"]').forEach((tab) => tab.setAttribute("aria-selected", String(tab.dataset.tab === state.tab)));
    root.querySelectorAll("[data-panel]").forEach((p) => { p.hidden = p.dataset.panel !== state.tab; });

    const picked = select();
    const id = await hashId(picked.map((t) => t.id));
    if (mine !== ticket) return;
    const fam = new Set(picked.map((t) => `${t.format}|${t.family}`)).size;
    summaryEl.innerHTML = `<span><b>${picked.length}</b>${T.targets}</span>
      <span><b>${new Set(picked.map((t) => t.format)).size}</b>${T.formats}</span>
      <span><b>${new Set(picked.map((t) => t.ecosystem)).size}</b>${T.ecosystems}</span>
      <span><b>${fam}</b>${T.families}</span>
      <span class="sel-id">${T.id} <code>${id}</code></span>`;
    const tablePanel = root.querySelector('[data-panel="targets"]');
    tablePanel.innerHTML = tableFor(picked);
    const moreButton = tablePanel.querySelector("[data-more]");
    if (moreButton) moreButton.addEventListener("click", () => { state.expanded = true; update(); });
    const script = scriptFor(id, picked);
    const manifest = manifestFor(id, picked);
    const report = reportFor(id, picked);
    root.querySelector('[data-out="script"]').textContent = script;
    root.querySelector('[data-out="manifest"]').textContent = manifest;
    root.querySelector('[data-out="runcmd"]').innerHTML =
      `<span class="p">$ </span>parsarium run-selection ${id}.json --mode ${state.mode}${state.mode === "afl" ? " --seconds 3600 --count 100" : ""}${state.mode === "fandango" ? " --count 100 --seed 42" : ""}${["file", "replay"].includes(state.mode) ? " --input PATH" : ""}`;
    root.querySelector('[data-out="report"]').textContent = report;
    setDownload("script", "run-selection.sh", script, "text/x-shellscript");
    setDownload("manifest", `${id}.json`, manifest, "application/json");
    setDownload("report", `${id}.md`, report, "text/markdown");
  }
  root.querySelectorAll("pre[data-out]").forEach((pre) => window.parsariumCopy && window.parsariumCopy(pre));
  update();
})();
