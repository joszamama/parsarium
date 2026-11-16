/* The teaching terminal runs browser decoders on the same pinned controls used
   by the repository's Docker harnesses. Saved harness results stay separate. */
(() => {
  "use strict";

  const root = document.querySelector("#lab-app");
  if (!root) return;
  const liveIds = ["png", "svg", "ascii_pnm"];
  const names = { png: "PNG", svg: "SVG", ascii_pnm: "ASCII PNM" };
  const engines = {
    png: "Browser image decoder + Canvas pixels",
    svg: "DOMParser + SVG element inspection",
    ascii_pnm: "Small P3 teaching decoder",
  };
  const encoder = new TextDecoder("utf-8", { fatal: true });
  const state = { catalog: null, demos: new Map(), format: null, data: null,
    structure: null, observed: null, swatches: [], busy: false,
    commands: [], commandIndex: 0, quizFormat: "png", explored: new Set() };
  const el = (selector) => root.querySelector(selector);
  const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[char]));
  const demoFor = (format) => state.demos.get(format);
  const localControlUrl = (demo) => new URL(`../${demo.controlUrl}`, document.baseURI).href;

  function shell() {
    root.innerHTML = `
      <div class="teach-layout">
        <div class="teach-live-options" aria-label="Live browser examples">
          <span>LOAD AN EXAMPLE</span>${liveIds.map((id) => `<button type="button" data-teach-command="load ${id}">${names[id]} <span aria-hidden="true">↗</span></button>`).join("")}
        </div>
        <div class="teach-workspace">
          <section class="teach-terminal" aria-labelledby="teach-terminal-title">
            <div class="teach-terminal-bar"><span class="teach-terminal-lights" aria-hidden="true"><i></i><i></i><i></i></span><h2 id="teach-terminal-title">Browser terminal</h2><span class="teach-live-badge">LIVE</span></div>
            <div class="teach-terminal-history" id="teach-terminal-history" role="log" aria-live="polite" aria-relevant="additions text"></div>
            <form id="teach-form" class="teach-terminal-form">
              <label for="teach-input">Command</label>
              <div><span aria-hidden="true">$</span><input id="teach-input" type="text" autocomplete="off" autocapitalize="off" spellcheck="false" aria-describedby="teach-hint" placeholder="try: parse"><button type="submit">Run <span aria-hidden="true">↵</span></button></div>
            </form>
            <p id="teach-hint" class="teach-hint">Try <code>help</code>, <code>bytes</code>, <code>parse</code>, or <code>result</code>. ↑ recalls a command.</p>
            <div class="teach-shortcuts" aria-label="Example commands"><button type="button" data-teach-command="bytes">bytes</button><button type="button" data-teach-command="parse">parse</button><button type="button" data-teach-command="result">result</button><button type="button" data-teach-command="reset">reset</button></div>
          </section>
          <section class="teach-visual" aria-labelledby="teach-visual-title">
            <div class="teach-visual-head"><div><span class="teach-overline">WHAT IS HAPPENING</span><h2 id="teach-visual-title">Inside the file</h2></div><span id="teach-format-badge" class="teach-format-badge">Waiting</span></div>
            <ol class="teach-pipeline" aria-label="Parsing stages"><li data-teach-stage="bytes"><b>Bytes</b><small>loaded control</small></li><li data-teach-stage="structure"><b>Structure</b><small>format grammar</small></li><li data-teach-stage="result"><b>Result</b><small>observed fields</small></li></ol>
            <div class="teach-panels">
              <div class="teach-panel" id="teach-bytes"><h3>Bytes</h3><p>Load a format to inspect its control.</p></div>
              <div class="teach-panel" id="teach-structure"><h3>Structure</h3><p>Run <code>parse</code> to see how the format is organized.</p></div>
              <div class="teach-panel" id="teach-result"><h3>Result</h3><p>The browser's observed fields will appear here.</p></div>
            </div>
          </section>
        </div>
        <aside class="teach-receipt" id="teach-receipt" aria-label="Saved Docker verification"></aside>
        <section class="teach-quiz" id="teach-quiz" aria-labelledby="teach-quiz-title"></section>
      </div>`;
  }

  function terminalLine(kind, value) {
    const history = el("#teach-terminal-history");
    const line = document.createElement("div");
    line.className = `teach-line teach-line-${kind}`;
    if (kind === "command") {
      const prompt = document.createElement("span");
      prompt.className = "teach-prompt";
      prompt.textContent = "$ ";
      line.append(prompt);
    }
    const body = document.createElement("span");
    body.textContent = value;
    line.append(body);
    history.append(line);
    history.scrollTop = history.scrollHeight;
  }

  function busy(value) {
    state.busy = value;
    el("#teach-input").disabled = value;
    el("#teach-form button").disabled = value;
    root.querySelectorAll("[data-teach-command]").forEach((button) => { button.disabled = value; });
  }

  function stage(which) {
    const order = ["bytes", "structure", "result"];
    const index = order.indexOf(which);
    root.querySelectorAll("[data-teach-stage]").forEach((item, position) => {
      item.classList.toggle("is-done", position <= index);
      item.classList.toggle("is-current", position === index);
    });
  }

  function hexDump(data, start = 0, count = 32) {
    const lines = [];
    for (let offset = start; offset < Math.min(start + count, data.length); offset += 16) {
      const chunk = data.slice(offset, Math.min(offset + 16, start + count));
      const hex = [...chunk].map((value) => value.toString(16).padStart(2, "0")).join(" ");
      const ascii = [...chunk].map((value) => value >= 32 && value < 127 ? String.fromCharCode(value) : "·").join("");
      lines.push(`${offset.toString(16).padStart(4, "0")}  ${hex.padEnd(47)}  ${ascii}`);
    }
    return lines.join("\n");
  }

  function byteTiles(data, start = 0, count = 32) {
    return [...data.slice(start, start + count)].map((value, index) => {
      const ascii = value >= 32 && value < 127 ? String.fromCharCode(value) : "·";
      return `<span class="teach-byte" style="--n:${index}"><b>${value.toString(16).toUpperCase().padStart(2, "0")}</b><small>${escapeHtml(ascii)}</small></span>`;
    }).join("");
  }

  function renderBytes(start = 0, count = 32) {
    if (!state.data) return;
    const demo = demoFor(state.format);
    const end = Math.min(start + count, state.data.length) - 1;
    const hex = [...state.data.slice(start, start + count)].map((value) => value.toString(16).toUpperCase().padStart(2, "0")).join(" ");
    el("#teach-bytes").innerHTML = `<h3>Bytes <span>${state.data.length} total</span></h3><p>${escapeHtml(demo.control)} · offsets ${start}–${end}</p><div class="teach-byte-grid" role="img" aria-label="Hexadecimal bytes ${start} through ${end}: ${hex}">${byteTiles(state.data, start, count)}</div>`;
  }

  function renderStructure(items) {
    el("#teach-structure").innerHTML = `<h3>Structure</h3><ul class="teach-structure-list">${items.map((item, index) => `<li style="--n:${index}"><strong>${escapeHtml(item.label)}</strong><span>${escapeHtml(item.detail)}</span></li>`).join("")}</ul>`;
  }

  function renderResult(output, swatches) {
    const colors = swatches.filter((color) => /^#[0-9a-fA-F]{6}$/.test(color));
    const strip = colors.length ? `<div class="teach-color-strip" aria-label="Observed pixel colors">${colors.map((color, index) => `<span style="background:${color}" title="${escapeHtml(color)}"><small>${index + 1}</small></span>`).join("")}</div>` : "";
    el("#teach-result").innerHTML = `<h3>Result <span>computed here</span></h3>${strip}<pre>${escapeHtml(JSON.stringify(output, null, 2))}</pre>`;
  }

  function savedReceipt(demo) {
    const guide = demo.projectGuideUrl;
    el("#teach-receipt").innerHTML = `<div><span class="teach-overline">SAVED VERIFICATION · DOCKER HARNESS</span><h2>Run the catalog target locally.</h2><p>This saved receipt comes from <strong>${escapeHtml(demo.package)} ${escapeHtml(demo.release)}</strong>. The live terminal above runs a browser decoder or teaching decoder; it does not run this container.</p><a href="${escapeHtml(guide)}" target="_blank" rel="noopener noreferrer">Read the pinned harness guide ↗</a></div><div class="teach-receipt-detail"><span>REPOSITORY COMMAND</span><code>${escapeHtml(demo.controlCommand)}</code><span>SAVED PARSER RESULT</span><pre>${escapeHtml(JSON.stringify(demo.expectedOutput, null, 2))}</pre></div>`;
  }

  async function loadFormat(format) {
    const demo = demoFor(format);
    if (!demo || !liveIds.includes(format)) throw new Error(`Live browser examples: ${liveIds.join(", ")}. Type formats for details.`);
    const response = await fetch(localControlUrl(demo));
    if (!response.ok) throw new Error(`Could not load ${demo.control} (HTTP ${response.status}).`);
    const data = new Uint8Array(await response.arrayBuffer());
    if (data.length !== demo.bytes) throw new Error(`Control size changed: expected ${demo.bytes}, received ${data.length}.`);
    state.format = format;
    state.data = data;
    state.structure = null;
    state.observed = null;
    state.swatches = [];
    el("#teach-format-badge").textContent = `${names[format]} · ${engines[format]}`;
    renderBytes();
    el("#teach-structure").innerHTML = `<h3>Structure</h3><p>Run <code>parse</code> to inspect the ${names[format]} structure.</p>`;
    el("#teach-result").innerHTML = `<h3>Result</h3><p>The observed fields will appear after parsing.</p>`;
    savedReceipt(demo);
    stage("bytes");
    const url = new URL(location.href);
    url.searchParams.set("format", format);
    history.replaceState(null, "", url);
    terminalLine("output", `Loaded ${demo.control} (${data.length} bytes). Try parse.`);
  }

  function pngStructure(data) {
    const signature = [137, 80, 78, 71, 13, 10, 26, 10];
    if (signature.some((value, index) => data[index] !== value)) throw new Error("The bytes do not begin with a PNG signature.");
    const view = new DataView(data.buffer, data.byteOffset, data.byteLength);
    const chunks = [{ label: "PNG signature", detail: "8 bytes · file identity" }];
    let offset = 8;
    while (offset + 12 <= data.length) {
      const length = view.getUint32(offset);
      if (offset + length + 12 > data.length) throw new Error("PNG chunk extends beyond the control file.");
      const type = String.fromCharCode(...data.slice(offset + 4, offset + 8));
      chunks.push({ label: type, detail: `${length} data bytes · offset ${offset}` });
      offset += length + 12;
      if (type === "IEND") break;
    }
    if (!chunks.some((chunk) => chunk.label === "IHDR")) throw new Error("PNG has no IHDR chunk.");
    return chunks;
  }

  async function parsePng(data) {
    const structure = pngStructure(data);
    const url = URL.createObjectURL(new Blob([data], { type: "image/png" }));
    try {
      const image = new Image();
      image.src = url;
      await image.decode();
      const canvas = document.createElement("canvas");
      canvas.width = image.naturalWidth;
      canvas.height = image.naturalHeight;
      const context = canvas.getContext("2d", { willReadFrequently: true });
      if (!context) throw new Error("This browser has no 2D Canvas context.");
      context.drawImage(image, 0, 0);
      const pixels = context.getImageData(0, 0, canvas.width, canvas.height).data;
      const first = Array.from(pixels.slice(0, 4));
      const second = Array.from(pixels.slice(4, 8));
      const toColor = (rgba) => `#${rgba.slice(0, 3).map((value) => value.toString(16).padStart(2, "0")).join("")}`;
      return { structure, output: { width: canvas.width, height: canvas.height, rgba0: first, rgba1: second },
        swatches: [toColor(first), toColor(second)] };
    } finally { URL.revokeObjectURL(url); }
  }

  function parseSvg(data) {
    const source = encoder.decode(data);
    const documentSvg = new DOMParser().parseFromString(source, "image/svg+xml");
    if (documentSvg.querySelector("parsererror")) throw new Error("The browser rejected the SVG XML.");
    const svg = documentSvg.documentElement;
    if (svg.namespaceURI !== "http://www.w3.org/2000/svg" || svg.localName !== "svg") throw new Error("No SVG root element found.");
    const width = Number(svg.getAttribute("width"));
    const height = Number(svg.getAttribute("height"));
    if (!(width > 0 && height > 0)) throw new Error("The control has no numeric SVG dimensions.");
    const rects = Array.from(svg.getElementsByTagNameNS("http://www.w3.org/2000/svg", "rect"));
    const structure = [{ label: "<svg>", detail: `${width} × ${height} viewport` },
      ...rects.map((rect, index) => ({ label: `<rect> ${index + 1}`, detail: `x=${rect.getAttribute("x")}, y=${rect.getAttribute("y")}, fill=${rect.getAttribute("fill")}` }))];
    return { structure, output: { width, height, nodes: rects.length,
      fills: rects.map((rect) => rect.getAttribute("fill")) },
    swatches: rects.map((rect) => rect.getAttribute("fill") || "") };
  }

  function parsePnm(data) {
    const text = encoder.decode(data);
    const words = text.replace(/#[^\r\n]*/g, " ").trim().split(/\s+/);
    if (words[0] !== "P3") throw new Error("This teaching decoder accepts ASCII color PNM (P3) only.");
    const values = words.slice(1).map(Number);
    const [width, height, maxval] = values;
    if (![width, height, maxval].every(Number.isInteger) || width < 1 || height < 1 || maxval < 1 || maxval > 65535) throw new Error("Invalid P3 dimensions or maxval.");
    const samples = values.slice(3);
    if (samples.length !== width * height * 3 || samples.some((value) => !Number.isInteger(value) || value < 0 || value > maxval)) throw new Error("P3 sample count or range does not match the header.");
    const scaled = samples.map((value) => Math.round(value * 255 / maxval));
    const rgb0 = scaled.slice(0, 3);
    const rgb1 = scaled.slice(3, 6);
    const toColor = (rgb) => `#${rgb.map((value) => value.toString(16).padStart(2, "0")).join("")}`;
    return { structure: [
      { label: "P3 magic", detail: "ASCII RGB samples" },
      { label: "Dimensions", detail: `${width} columns × ${height} row${height === 1 ? "" : "s"}` },
      { label: "Maxval", detail: `${maxval} is the largest channel value` },
      { label: "Pixels", detail: `${width * height} RGB triples follow the header` },
    ], output: { width, height, maxval, rgb0, rgb1 }, swatches: [toColor(rgb0), toColor(rgb1)] };
  }

  async function parseLoaded() {
    if (!state.data) throw new Error("Load a control first, for example: load png");
    const parsed = state.format === "png" ? await parsePng(state.data)
      : state.format === "svg" ? parseSvg(state.data) : parsePnm(state.data);
    state.structure = parsed.structure;
    state.observed = parsed.output;
    state.swatches = parsed.swatches;
    renderStructure(parsed.structure);
    stage("structure");
    if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      await new Promise((resolve) => setTimeout(resolve, 420));
    }
    renderResult(parsed.output, parsed.swatches);
    stage("result");
    terminalLine("success", `Parsed ${names[state.format]} with ${engines[state.format]}.\n${JSON.stringify(parsed.output, null, 2)}`);
  }

  async function execute(raw) {
    const command = raw.trim();
    if (!command) return;
    terminalLine("command", command);
    state.commands.push(command);
    state.commandIndex = state.commands.length;
    const parts = command.toLowerCase().split(/\s+/);
    try {
      busy(true);
      switch (parts[0]) {
        case "help":
          terminalLine("output", "load png | load svg | load ascii_pnm  — fetch a pinned control\nbytes [offset] [count]  — inspect 8–64 bytes\nparse  — run the browser or teaching decoder\nresult  — print the live result again\nformats  — list live formats\nreset  — clear the terminal session");
          break;
        case "formats":
          terminalLine("output", "Live here: png (browser image decoder), svg (DOMParser), ascii_pnm (P3 teaching decoder). All ten formats also have byte-clue lessons below.");
          break;
        case "load":
          if (parts.length !== 2) throw new Error("Usage: load png | load svg | load ascii_pnm");
          await loadFormat(parts[1]);
          break;
        case "bytes": {
          if (!state.data) throw new Error("Load a control first, for example: load png");
          const offset = parts[1] === undefined ? 0 : Number(parts[1]);
          const count = parts[2] === undefined ? 32 : Number(parts[2]);
          if (parts.length > 3 || !Number.isInteger(offset) || offset < 0 || offset >= state.data.length || !Number.isInteger(count) || count < 8 || count > 64) throw new Error(`Usage: bytes [offset 0–${state.data.length - 1}] [count 8–64]`);
          renderBytes(offset, count);
          stage(state.observed ? "result" : "bytes");
          terminalLine("output", hexDump(state.data, offset, count));
          break;
        }
        case "parse":
          if (parts.length !== 1) throw new Error("Usage: parse");
          await parseLoaded();
          break;
        case "result":
          if (!state.observed) throw new Error("Run parse first to produce an observed result.");
          terminalLine("output", JSON.stringify(state.observed, null, 2));
          break;
        case "reset":
          if (parts.length !== 1) throw new Error("Usage: reset");
          state.format = null; state.data = null; state.structure = null; state.observed = null; state.swatches = [];
          state.commands = []; state.commandIndex = 0;
          el("#teach-format-badge").textContent = "Waiting";
          el("#teach-bytes").innerHTML = "<h3>Bytes</h3><p>Load a format to inspect its control.</p>";
          el("#teach-structure").innerHTML = "<h3>Structure</h3><p>Run <code>parse</code> to see how the format is organized.</p>";
          el("#teach-result").innerHTML = "<h3>Result</h3><p>The browser's observed fields will appear here.</p>";
          el("#teach-receipt").innerHTML = "";
          el("#teach-terminal-history").innerHTML = "";
          stage(null);
          const resetUrl = new URL(location.href);
          resetUrl.searchParams.delete("format");
          history.replaceState(null, "", resetUrl);
          terminalLine("output", "Terminal session cleared. Try load png.");
          break;
        default:
          if (["python3", "docker", "parsarium.py"].includes(parts[0])) throw new Error("Docker harness commands run on your computer, not in this browser. See the saved verification panel and Run page.");
          throw new Error(`Unknown command: ${parts[0]}. Type help to list the commands.`);
      }
    } catch (error) {
      terminalLine("error", error instanceof Error ? error.message : String(error));
    } finally {
      busy(false);
      el("#teach-input").focus();
    }
  }

  function quiz() {
    const demo = demoFor(state.quizFormat);
    const lesson = demo.lesson;
    const complete = state.explored.has(state.quizFormat);
    const label = state.catalog.formats.find((format) => format.id === state.quizFormat)?.label || state.quizFormat;
    const clue = lesson.tokens.filter((token) => token.focus);
    const clueHex = clue.map((token) => token.hex).join(" ");
    const clueAscii = clue.map((token) => token.ascii).join("");
    el("#teach-quiz").innerHTML = `
      <div class="teach-quiz-header"><div><span class="teach-overline">TEN SMALL FORMAT LESSONS</span><h2 id="teach-quiz-title">Decode a clue.</h2><p>Choose a format. These highlighted bytes come from its real pinned control; the answer is a saved parser observation.</p></div><strong>${state.explored.size} / ${state.catalog.demos.length} explored</strong></div>
      <label class="teach-quiz-picker">FORMAT <select id="teach-quiz-select">${state.catalog.demos.map((item) => `<option value="${escapeHtml(item.format)}" ${item.format === state.quizFormat ? "selected" : ""}>${escapeHtml(state.catalog.formats.find((format) => format.id === item.format)?.label || item.format)}</option>`).join("")}</select></label>
      <div class="teach-quiz-body"><div class="teach-quiz-file"><span class="teach-overline">${escapeHtml(label)} · ${escapeHtml(demo.control.split("/").pop())}</span><div class="teach-quiz-bytes" role="img" aria-label="Highlighted control bytes at offset ${lesson.clueOffset}: hex ${escapeHtml(clueHex)}, ASCII ${escapeHtml(clueAscii)}">${lesson.tokens.map((token, index) => `<span class="teach-byte ${token.focus ? "is-clue" : ""}" style="--n:${index}" aria-hidden="true"><b>${escapeHtml(token.hex)}</b><small>${escapeHtml(token.ascii)}</small></span>`).join("")}</div><p>Clue starts at byte offset <b>${lesson.clueOffset}</b>. <a href="${escapeHtml(localControlUrl(demo))}" target="_blank" rel="noopener noreferrer">Open control ↗</a></p></div>
      <div class="teach-quiz-answer"><h3>${escapeHtml(lesson.question)}</h3><div class="teach-quiz-choices">${lesson.choices.map((choice, index) => `<button type="button" data-teach-choice="${index}" ${complete ? "disabled" : ""} class="${complete && index === lesson.answer ? "is-correct" : ""}">${escapeHtml(choice)}</button>`).join("")}</div><p id="teach-quiz-feedback" role="status">${complete ? "Explanation revealed." : "Choose an answer or reveal the explanation."}</p><button type="button" class="teach-quiz-reveal" data-teach-reveal ${complete ? "hidden" : ""}>Reveal explanation</button>${complete ? `<div class="teach-quiz-explanation"><strong>Saved parser receipt</strong><p>${escapeHtml(lesson.explanation)}</p><pre>${escapeHtml(JSON.stringify(lesson.output, null, 2))}</pre></div>` : ""}</div></div>`;
  }

  function answerQuiz(index) {
    if (state.explored.has(state.quizFormat)) return;
    const lesson = demoFor(state.quizFormat).lesson;
    if (index === lesson.answer) {
      state.explored.add(state.quizFormat);
      quiz();
    } else {
      el(`[data-teach-choice="${index}"]`).classList.add("is-wrong");
      el("#teach-quiz-feedback").textContent = "That field belongs to another format. Try again.";
    }
  }

  function wire() {
    el("#teach-form").addEventListener("submit", (event) => {
      event.preventDefault();
      const input = el("#teach-input");
      const command = input.value.trim();
      input.value = "";
      if (!state.busy && command) void execute(command);
    });
    el("#teach-input").addEventListener("keydown", (event) => {
      if (event.key === "ArrowUp" && state.commands.length) {
        event.preventDefault();
        state.commandIndex = Math.max(0, state.commandIndex - 1);
        event.currentTarget.value = state.commands[state.commandIndex];
      } else if (event.key === "ArrowDown" && state.commands.length) {
        event.preventDefault();
        state.commandIndex = Math.min(state.commands.length, state.commandIndex + 1);
        event.currentTarget.value = state.commands[state.commandIndex] || "";
      }
    });
    root.addEventListener("click", (event) => {
      const shortcut = event.target.closest("[data-teach-command]");
      if (shortcut && !state.busy) void execute(shortcut.dataset.teachCommand);
      const choice = event.target.closest("[data-teach-choice]");
      if (choice) answerQuiz(Number(choice.dataset.teachChoice));
      if (event.target.closest("[data-teach-reveal]")) {
        state.explored.add(state.quizFormat);
        quiz();
      }
    });
    root.addEventListener("change", (event) => {
      if (event.target.matches("#teach-quiz-select")) {
        state.quizFormat = event.target.value;
        quiz();
      }
    });
  }

  async function init() {
    root.innerHTML = '<p class="teach-loading" role="status">Loading the pinned control catalog…</p>';
    try {
      const response = await fetch(new URL("../catalog.json", document.baseURI));
      if (!response.ok) throw new Error(`catalog HTTP ${response.status}`);
      state.catalog = await response.json();
      state.demos = new Map(state.catalog.demos.map((demo) => [demo.format, demo]));
      if (liveIds.some((id) => !state.demos.has(id)) || state.catalog.demos.some((demo) => !demo.lesson)) throw new Error("catalog is missing a teaching control");
      const requested = new URL(location.href).searchParams.get("format");
      const initial = liveIds.includes(requested) ? requested : "png";
      state.quizFormat = requested && state.demos.has(requested) ? requested : initial;
      shell();
      wire();
      quiz();
      terminalLine("welcome", "Parsarium browser lab. Type help for commands. Loading a pinned control now…");
      await execute(`load ${initial}`);
    } catch (error) {
      root.innerHTML = `<p class="teach-loading teach-loading-error" role="alert">The teaching catalog could not be loaded. ${escapeHtml(error instanceof Error ? error.message : String(error))}</p>`;
    }
  }
  void init();
})();
