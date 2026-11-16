/* The teaching terminal runs browser decoders on the same pinned controls used
   by the repository's Docker harnesses. Saved harness results stay separate. */
(() => {
  "use strict";

  const root = document.querySelector("#lab-app");
  if (!root) return;
  const es = document.body.dataset.lang === "es";
  const tr = (english, spanish) => es ? spanish : english;
  const assetRoot = document.body.dataset.root || "../";
  const localeRoot = document.body.dataset.localeRoot || "../";
  const liveIds = ["png", "svg", "ascii_pnm"];
  const names = { png: "PNG", svg: "SVG", ascii_pnm: tr("ASCII PNM", "PNM ASCII") };
  const engines = {
    png: tr("Browser image decoder + Canvas pixels", "Decodificador del navegador + píxeles de Canvas"),
    svg: tr("DOMParser + SVG element inspection", "DOMParser + inspección de elementos SVG"),
    ascii_pnm: tr("Small P3 teaching decoder", "Pequeño decodificador didáctico de P3"),
  };
  const lessonEs = {
    png: { question: "¿Qué describe el bloque IHDR?", choices: ["Dimensiones y modo de color de la imagen", "Entradas del archivo ZIP", "Frecuencia de muestreo del audio"], explanation: "IHDR es un bloque obligatorio de PNG. Contiene anchura, altura, profundidad de bits y tipo de color." },
    zip: { question: "¿Qué ayuda a encontrar este registro ZIP?", choices: ["Un color de píxel", "La tabla de entradas del archivo", "Un host HTTP"], explanation: "El directorio central registra las entradas del archivo y dónde están sus datos locales." },
    mp4: { question: "¿Qué contiene la caja moov?", choices: ["El árbol de páginas PDF", "Un nombre de archivo ZIP", "Metadatos de pistas y tiempos"], explanation: "MP4 se compone de cajas anidadas. moov contiene metadatos de la película y sus pistas para interpretar el contenido." },
    wav: { question: "¿Qué indica el bloque fmt a un lector WAV?", choices: ["El nivel de compresión del archivo", "La codificación de muestras y la disposición de canales", "El número de páginas"], explanation: "fmt describe cómo interpretar las muestras: frecuencia, número de canales y formato de muestra." },
    pdf: { question: "¿Qué significa /Count 1 en este árbol de páginas?", choices: ["El archivo tiene un byte", "Hay una fuente", "Hay una página bajo este nodo"], explanation: "El árbol de páginas PDF usa /Count para indicar cuántas páginas descendientes hay. El parser resuelve esa estructura." },
    svg: { question: "¿Qué fijan estos atributos de la raíz SVG?", choices: ["El tamaño de una entrada ZIP", "Las dimensiones del área visible", "La longitud del cuerpo HTTP"], explanation: "La raíz SVG da las dimensiones de la imagen; los elementos hijos describen las formas vectoriales dentro de ese espacio." },
    http11: { question: "¿Qué identifica esta cabecera?", choices: ["El códec de audio", "La anchura de la imagen", "El host solicitado"], explanation: "Una petición HTTP/1.1 tiene una línea inicial y cabeceras. Host identifica el nombre del servidor solicitado." },
    ascii_ply: { question: "¿Qué declara esta línea de cabecera PLY?", choices: ["Siguen tres píxeles", "Siguen tres registros de vértices", "Siguen tres canales de audio"], explanation: "La cabecera PLY ASCII declara la disposición de los registros antes de leer las líneas de vértices y caras." },
    ascii_pnm: { question: "¿Qué selecciona el valor mágico P3?", choices: ["Un bloque PNG comprimido", "Un campo de título ID3", "Muestras RGB en ASCII"], explanation: "P3 identifica una imagen PNM en color y texto. Después, el lector usa las dimensiones, el valor máximo y las tripletas de muestras." },
    mp3_id3v2: { question: "¿Qué contiene este campo ID3v2?", choices: ["La frecuencia de muestreo MP3", "El título de la pista", "La longitud del archivo"], explanation: "TIT2 es el campo de título ID3v2. En este control aparece en la etiqueta anterior a los fotogramas de audio." },
  };
  const encoder = new TextDecoder("utf-8", { fatal: true });
  const state = { catalog: null, demos: new Map(), format: null, data: null,
    structure: null, observed: null, revealed: false, swatches: [], busy: false,
    commands: [], commandIndex: 0, quizFormat: "png", explored: new Set() };
  const el = (selector) => root.querySelector(selector);
  const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[char]));
  const demoFor = (format) => state.demos.get(format);
  const localControlUrl = (demo) => new URL(`${assetRoot}${demo.controlUrl}`, document.baseURI).href;

  function shell() {
    root.innerHTML = `
      <div class="teach-layout">
        <div class="teach-live-options" aria-label="${tr("Live browser examples", "Ejemplos interactivos en el navegador")}">
          <span>${tr("LOAD AN EXAMPLE", "CARGA UN EJEMPLO")}</span>${liveIds.map((id) => `<button type="button" data-teach-command="load ${id}">${names[id]} <span aria-hidden="true">↗</span></button>`).join("")}
        </div>
        <div class="teach-workspace">
          <section class="teach-terminal" aria-labelledby="teach-terminal-title">
            <div class="teach-terminal-bar"><span class="teach-terminal-lights" aria-hidden="true"><i></i><i></i><i></i></span><h2 id="teach-terminal-title">Terminal</h2><span class="teach-live-badge">${tr("IN BROWSER", "EN EL NAVEGADOR")}</span></div>
            <div class="teach-terminal-history" id="teach-terminal-history" role="log" aria-live="polite" aria-relevant="additions text"></div>
            <form id="teach-form" class="teach-terminal-form">
              <label for="teach-input">${tr("Command", "Comando")}</label>
              <div><span aria-hidden="true">$</span><input id="teach-input" type="text" autocomplete="off" autocapitalize="off" spellcheck="false" aria-describedby="teach-hint" placeholder="${tr("try: parse", "prueba: parse")}"><button type="submit">${tr("Run", "Ejecutar")} <span aria-hidden="true">↵</span></button></div>
            </form>
            <p id="teach-hint" class="teach-hint">${tr("Try", "Prueba")} <code>parse</code> ${tr("to inspect structure. Use", "para inspeccionar la estructura. Usa")} <code>result</code> ${tr("only when you are ready to see the observed fields. ↑ recalls a command.", "cuando quieras ver los campos observados. ↑ recupera un comando anterior.")}</p>
            <div class="teach-shortcuts" aria-label="${tr("Example commands", "Comandos de ejemplo")}"><button type="button" data-teach-command="bytes">bytes</button><button type="button" data-teach-command="parse">parse</button><button type="button" data-teach-command="result">result</button><button type="button" data-teach-command="reset">reset</button></div>
          </section>
          <section class="teach-visual" aria-labelledby="teach-visual-title">
            <div class="teach-visual-head"><div><span class="teach-overline">${tr("WHAT IS HAPPENING", "QUÉ ESTÁ PASANDO")}</span><h2 id="teach-visual-title">${tr("Inside the file", "Dentro del archivo")}</h2></div><span id="teach-format-badge" class="teach-format-badge">${tr("Waiting", "Esperando")}</span></div>
            <ol class="teach-pipeline" aria-label="${tr("Parsing stages", "Etapas del parsing")}"><li data-teach-stage="bytes"><b>Bytes</b><small>${tr("loaded control", "control cargado")}</small></li><li data-teach-stage="structure"><b>${tr("Structure", "Estructura")}</b><small>${tr("format grammar", "gramática del formato")}</small></li><li data-teach-stage="result"><b>${tr("Result", "Resultado")}</b><small>${tr("observed fields", "campos observados")}</small></li></ol>
            <div class="teach-panels">
              <div class="teach-panel" id="teach-bytes"><h3>Bytes</h3><p>${tr("Load a format to inspect its control.", "Carga un formato para inspeccionar su control.")}</p></div>
              <div class="teach-panel" id="teach-structure"><h3>${tr("Format grammar", "Gramática del formato")}</h3><p>${tr("Run", "Ejecuta")} <code>parse</code> ${tr("to see how the format is organized.", "para ver cómo se organiza el formato.")}</p></div>
              <div class="teach-panel" id="teach-result"><h3>${tr("Result", "Resultado")}</h3><p>${tr("First inspect the grammar. Then choose when to reveal the parser result.", "Inspecciona primero la gramática. Después, decide cuándo revelar el resultado del parser.")}</p></div>
            </div>
          </section>
        </div>
        <aside class="teach-next-step" id="teach-next-step" aria-label="${tr("Continue with a runnable target", "Continuar con un objetivo ejecutable")}"></aside>
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
    el("#teach-bytes").innerHTML = `<h3>Bytes <span>${state.data.length} ${tr("total", "en total")}</span></h3><p>${escapeHtml(demo.control)} · ${tr("offsets", "posiciones")} ${start}–${end}</p><div class="teach-byte-grid" role="img" aria-label="${tr("Hexadecimal bytes", "Bytes hexadecimales")} ${start} ${tr("through", "a")} ${end}: ${hex}">${byteTiles(state.data, start, count)}</div>`;
  }

  function renderStructure(items) {
    const explanations = {
      png: tr("The signature identifies PNG. The parser then walks chunks; each chunk declares a length and type before its data and checksum.", "La firma identifica PNG. Después, el parser recorre bloques; cada uno declara su longitud y tipo antes de sus datos y suma de comprobación."),
      svg: tr("The XML parser builds an element tree. The SVG root and rectangle attributes provide the structure inspected here.", "El parser XML construye un árbol de elementos. La raíz SVG y los atributos de los rectángulos proporcionan la estructura que inspeccionamos."),
      ascii_pnm: tr("The P3 magic value starts an ordered sequence of text tokens: dimensions, maxval, then exactly enough RGB samples.", "El valor mágico P3 inicia una secuencia de tokens: dimensiones, valor máximo y las muestras RGB necesarias."),
    };
    el("#teach-structure").innerHTML = `<h3>${tr("Format grammar", "Gramática del formato")}</h3><p class="teach-grammar-note">${escapeHtml(explanations[state.format])}</p><ul class="teach-structure-list">${items.map((item, index) => `<li style="--n:${index}"><strong>${escapeHtml(item.label)}</strong><span>${escapeHtml(item.detail)}</span></li>`).join("")}</ul><button class="teach-reveal-result" type="button" data-teach-command="result">${tr("Continue to result", "Continuar al resultado")} →</button>`;
  }

  function renderResult(output, swatches) {
    const colors = swatches.filter((color) => /^#[0-9a-fA-F]{6}$/.test(color));
    const strip = colors.length ? `<div class="teach-color-strip" aria-label="${tr("Observed pixel colors", "Colores de píxeles observados")}">${colors.map((color, index) => `<span style="background:${color}" title="${escapeHtml(color)}"><small>${index + 1}</small></span>`).join("")}</div>` : "";
    el("#teach-result").innerHTML = `<h3>${tr("Result", "Resultado")} <span>${tr("computed here", "calculado aquí")}</span></h3>${strip}<pre>${escapeHtml(JSON.stringify(output, null, 2))}</pre>`;
  }

  function nextStep(demo) {
    const runUrl = new URL(`${localeRoot}run/?format=${encodeURIComponent(demo.format)}`, document.baseURI).href;
    el("#teach-next-step").innerHTML = `<div><span class="teach-overline">${tr("FROM LESSON TO TARGET", "DE LA LECCIÓN AL OBJETIVO")}</span><h2>${tr("Test the actual library.", "Prueba la biblioteca real.")}</h2><p>${tr("The example above uses a browser decoder or small teaching decoder. Run locally opens a pinned", "El ejemplo anterior usa un decodificador del navegador o uno didáctico. Ejecutar localmente abre un harness fijado de")} <strong>${escapeHtml(demo.package)}</strong> ${tr("harness for this format, with a valid control and coverage feedback.", "para este formato, con un control válido y feedback de cobertura.")}</p><a href="${escapeHtml(runUrl)}">${tr("Open Run locally", "Abrir Ejecutar") } ↗</a></div><div class="teach-next-step-detail"><span>${tr("HERE IN THE BROWSER", "AQUÍ EN EL NAVEGADOR")}</span><p>${tr("Watch parsing steps and inspect the control.", "Observa las etapas del parsing e inspecciona el control.")}</p><span>${tr("THERE ON YOUR MACHINE", "ALLÍ EN TU ORDENADOR")}</span><p>${tr("Run a library on your own file or corpus in Docker.", "Ejecuta una biblioteca con tu archivo o corpus en Docker.")}</p></div>`;
  }

  async function loadFormat(format) {
    const demo = demoFor(format);
    if (!demo || !liveIds.includes(format)) throw new Error(`${tr("Live browser examples", "Ejemplos interactivos")}: ${liveIds.join(", ")}. ${tr("Type formats for details.", "Escribe formats para verlos.")}`);
    const response = await fetch(localControlUrl(demo));
    if (!response.ok) throw new Error(`${tr("Could not load", "No se pudo cargar")} ${demo.control} (HTTP ${response.status}).`);
    const data = new Uint8Array(await response.arrayBuffer());
    if (data.length !== demo.bytes) throw new Error(`${tr("Control size changed: expected", "Cambió el tamaño del control: se esperaban")} ${demo.bytes}, ${tr("received", "se recibieron")} ${data.length}.`);
    state.format = format;
    state.data = data;
    state.structure = null;
    state.observed = null;
    state.revealed = false;
    state.swatches = [];
    el("#teach-format-badge").textContent = `${names[format]} · ${engines[format]}`;
    renderBytes();
    el("#teach-structure").innerHTML = `<h3>${tr("Format grammar", "Gramática del formato")}</h3><p>${tr("Run", "Ejecuta")} <code>parse</code> ${tr("to inspect the", "para inspeccionar la estructura de")} ${names[format]}.</p>`;
    el("#teach-result").innerHTML = `<h3>${tr("Result", "Resultado")}</h3><p>${tr("First inspect the grammar. Then choose when to reveal the parser result.", "Inspecciona primero la gramática. Después, decide cuándo revelar el resultado del parser.")}</p>`;
    nextStep(demo);
    stage("bytes");
    const url = new URL(location.href);
    url.searchParams.set("format", format);
    history.replaceState(null, "", url);
    terminalLine("output", `${tr("Loaded", "Cargado")} ${demo.control} (${data.length} bytes). ${tr("Try parse.", "Prueba parse.")}`);
  }

  function pngStructure(data) {
    const signature = [137, 80, 78, 71, 13, 10, 26, 10];
    if (signature.some((value, index) => data[index] !== value)) throw new Error(tr("The bytes do not begin with a PNG signature.", "La entrada no comienza con una firma PNG."));
    const view = new DataView(data.buffer, data.byteOffset, data.byteLength);
    const chunks = [{ label: tr("PNG signature", "Firma PNG"), detail: tr("8 bytes · file identity", "8 bytes · identidad del archivo") }];
    let offset = 8;
    while (offset + 12 <= data.length) {
      const length = view.getUint32(offset);
      if (offset + length + 12 > data.length) throw new Error(tr("PNG chunk extends beyond the control file.", "Un bloque PNG sobrepasa el archivo de control."));
      const type = String.fromCharCode(...data.slice(offset + 4, offset + 8));
      chunks.push({ label: type, detail: `${length} ${tr("data bytes · offset", "bytes de datos · posición")} ${offset}` });
      offset += length + 12;
      if (type === "IEND") break;
    }
    if (!chunks.some((chunk) => chunk.label === "IHDR")) throw new Error(tr("PNG has no IHDR chunk.", "El PNG no contiene un bloque IHDR."));
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
      if (!context) throw new Error(tr("This browser has no 2D Canvas context.", "Este navegador no dispone de un contexto Canvas 2D."));
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
    if (documentSvg.querySelector("parsererror")) throw new Error(tr("The browser rejected the SVG XML.", "El navegador rechazó el XML del SVG."));
    const svg = documentSvg.documentElement;
    if (svg.namespaceURI !== "http://www.w3.org/2000/svg" || svg.localName !== "svg") throw new Error(tr("No SVG root element found.", "No se encontró un elemento raíz SVG."));
    const width = Number(svg.getAttribute("width"));
    const height = Number(svg.getAttribute("height"));
    if (!(width > 0 && height > 0)) throw new Error(tr("The control has no numeric SVG dimensions.", "El control no tiene dimensiones SVG numéricas."));
    const rects = Array.from(svg.getElementsByTagNameNS("http://www.w3.org/2000/svg", "rect"));
    const structure = [{ label: "<svg>", detail: `${width} × ${height} ${tr("viewport", "área visible")}` },
      ...rects.map((rect, index) => ({ label: `<rect> ${index + 1}`, detail: `x=${rect.getAttribute("x")}, y=${rect.getAttribute("y")}, fill=${rect.getAttribute("fill")}` }))];
    return { structure, output: { width, height, nodes: rects.length,
      fills: rects.map((rect) => rect.getAttribute("fill")) },
    swatches: rects.map((rect) => rect.getAttribute("fill") || "") };
  }

  function parsePnm(data) {
    const text = encoder.decode(data);
    const words = text.replace(/#[^\r\n]*/g, " ").trim().split(/\s+/);
    if (words[0] !== "P3") throw new Error(tr("This teaching decoder accepts ASCII color PNM (P3) only.", "Este decodificador didáctico solo acepta PNM ASCII en color (P3)."));
    const values = words.slice(1).map(Number);
    const [width, height, maxval] = values;
    if (![width, height, maxval].every(Number.isInteger) || width < 1 || height < 1 || maxval < 1 || maxval > 65535) throw new Error(tr("Invalid P3 dimensions or maxval.", "Dimensiones o valor máximo P3 inválidos."));
    const samples = values.slice(3);
    if (samples.length !== width * height * 3 || samples.some((value) => !Number.isInteger(value) || value < 0 || value > maxval)) throw new Error(tr("P3 sample count or range does not match the header.", "El número o rango de muestras P3 no coincide con la cabecera."));
    const scaled = samples.map((value) => Math.round(value * 255 / maxval));
    const rgb0 = scaled.slice(0, 3);
    const rgb1 = scaled.slice(3, 6);
    const toColor = (rgb) => `#${rgb.map((value) => value.toString(16).padStart(2, "0")).join("")}`;
    return { structure: [
      { label: tr("P3 magic", "Valor mágico P3"), detail: tr("ASCII RGB samples", "Muestras RGB en ASCII") },
      { label: tr("Dimensions", "Dimensiones"), detail: es ? `${width} columnas × ${height} filas` : `${width} columns × ${height} row${height === 1 ? "" : "s"}` },
      { label: tr("Maxval", "Valor máximo"), detail: `${maxval} ${tr("is the largest channel value", "es el valor máximo de un canal")}` },
      { label: tr("Pixels", "Píxeles"), detail: `${width * height} ${tr("RGB triples follow the header", "tripletas RGB siguen a la cabecera")}` },
    ], output: { width, height, maxval, rgb0, rgb1 }, swatches: [toColor(rgb0), toColor(rgb1)] };
  }

  async function parseLoaded() {
    if (!state.data) throw new Error(tr("Load a control first, for example: load png", "Carga primero un control, por ejemplo: load png"));
    const parsed = state.format === "png" ? await parsePng(state.data)
      : state.format === "svg" ? parseSvg(state.data) : parsePnm(state.data);
    state.structure = parsed.structure;
    state.observed = parsed.output;
    state.revealed = false;
    state.swatches = parsed.swatches;
    renderStructure(parsed.structure);
    stage("structure");
    el("#teach-result").innerHTML = `<h3>${tr("Result", "Resultado")}</h3><p>${tr("The", "El")} ${names[state.format]} ${tr("result is ready. Review the format grammar, then type", "ya tiene un resultado. Revisa la gramática y después escribe")} <code>result</code> ${tr("or use the Continue button.", "o pulsa Continuar.")}</p>`;
    terminalLine("success", `${tr("Parsed", "Analizado")} ${names[state.format]} ${tr("with", "con")} ${engines[state.format]}. ${tr("Found", "Encontradas")} ${parsed.structure.length} ${tr("structure parts. Inspect the grammar, then type result when ready.", "partes de la estructura. Inspecciona la gramática y escribe result cuando quieras.")}`);
  }

  async function execute(raw, focusInput = false) {
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
          terminalLine("output", tr("load png | load svg | load ascii_pnm  — fetch a pinned control\nbytes [offset] [count]  — inspect 8–64 bytes\nparse  — reveal the format grammar\nresult  — reveal the observed fields\nformats  — list live formats\nreset  — clear the terminal session", "load png | load svg | load ascii_pnm  — cargar un control fijado\nbytes [offset] [count]  — inspeccionar 8–64 bytes\nparse  — revelar la gramática del formato\nresult  — revelar los campos observados\nformats  — mostrar los formatos interactivos\nreset  — limpiar la sesión del terminal"));
          break;
        case "formats":
          terminalLine("output", tr("Live here: png (browser image decoder), svg (DOMParser), ascii_pnm (P3 teaching decoder). All ten formats also have control-file questions below.", "Disponibles aquí: png (decodificador del navegador), svg (DOMParser), ascii_pnm (decodificador didáctico P3). Los diez formatos tienen además preguntas sobre sus controles más abajo."));
          break;
        case "load":
          if (parts.length !== 2) throw new Error(tr("Usage", "Uso") + ": load png | load svg | load ascii_pnm");
          await loadFormat(parts[1]);
          break;
        case "bytes": {
          if (!state.data) throw new Error(tr("Load a control first, for example: load png", "Carga primero un control, por ejemplo: load png"));
          const offset = parts[1] === undefined ? 0 : Number(parts[1]);
          const count = parts[2] === undefined ? 32 : Number(parts[2]);
          if (parts.length > 3 || !Number.isInteger(offset) || offset < 0 || offset >= state.data.length || !Number.isInteger(count) || count < 8 || count > 64) throw new Error(`${tr("Usage", "Uso")}: bytes [offset 0–${state.data.length - 1}] [count 8–64]`);
          renderBytes(offset, count);
          stage(state.revealed ? "result" : state.structure ? "structure" : "bytes");
          terminalLine("output", hexDump(state.data, offset, count));
          break;
        }
        case "parse":
          if (parts.length !== 1) throw new Error(`${tr("Usage", "Uso")}: parse`);
          await parseLoaded();
          break;
        case "result":
          if (!state.observed) throw new Error(tr("Run parse first to produce an observed result.", "Ejecuta parse primero para producir un resultado observado."));
          renderResult(state.observed, state.swatches);
          el(".teach-reveal-result")?.remove();
          state.revealed = true;
          stage("result");
          terminalLine("output", JSON.stringify(state.observed, null, 2));
          break;
        case "reset":
          if (parts.length !== 1) throw new Error(`${tr("Usage", "Uso")}: reset`);
          state.format = null; state.data = null; state.structure = null; state.observed = null; state.revealed = false; state.swatches = [];
          state.commands = []; state.commandIndex = 0;
          el("#teach-format-badge").textContent = tr("Waiting", "Esperando");
          el("#teach-bytes").innerHTML = `<h3>Bytes</h3><p>${tr("Load a format to inspect its control.", "Carga un formato para inspeccionar su control.")}</p>`;
          el("#teach-structure").innerHTML = `<h3>${tr("Format grammar", "Gramática del formato")}</h3><p>${tr("Run", "Ejecuta")} <code>parse</code> ${tr("to see how the format is organized.", "para ver cómo se organiza el formato.")}</p>`;
          el("#teach-result").innerHTML = `<h3>${tr("Result", "Resultado")}</h3><p>${tr("First inspect the grammar. Then choose when to reveal the parser result.", "Inspecciona primero la gramática. Después, decide cuándo revelar el resultado del parser.")}</p>`;
          el("#teach-next-step").innerHTML = "";
          el("#teach-terminal-history").innerHTML = "";
          stage(null);
          const resetUrl = new URL(location.href);
          resetUrl.searchParams.delete("format");
          history.replaceState(null, "", resetUrl);
          terminalLine("output", tr("Terminal session cleared. Try load png.", "Sesión del terminal reiniciada. Prueba load png."));
          break;
        default:
          if (["python3", "docker", "parsarium.py"].includes(parts[0])) throw new Error(tr("Docker harness commands run on your computer, not in this browser. See the saved verification panel and Run page.", "Los comandos del harness Docker se ejecutan en tu ordenador, no en este navegador. Consulta el panel de verificación y la página Ejecutar."));
          throw new Error(`${tr("Unknown command", "Comando desconocido")}: ${parts[0]}. ${tr("Type help to list the commands.", "Escribe help para ver los comandos.")}`);
      }
    } catch (error) {
      terminalLine("error", error instanceof Error ? error.message : String(error));
    } finally {
      busy(false);
      if (focusInput) el("#teach-input").focus();
    }
  }

  function quiz() {
    const demo = demoFor(state.quizFormat);
    const lesson = demo.lesson;
    const lessonCopy = es ? lessonEs[state.quizFormat] : lesson;
    const complete = state.explored.has(state.quizFormat);
    const label = state.catalog.formats.find((format) => format.id === state.quizFormat)?.label || state.quizFormat;
    const clue = lesson.tokens.filter((token) => token.focus);
    const clueHex = clue.map((token) => token.hex).join(" ");
    const clueAscii = clue.map((token) => token.ascii).join("");
    el("#teach-quiz").innerHTML = `
      <div class="teach-quiz-header"><div><span class="teach-overline">${tr("FIELD NOTES · ALL TEN FORMATS", "NOTAS · LOS DIEZ FORMATOS")}</span><h2 id="teach-quiz-title">${tr("Test a clue.", "Pon a prueba una pista.")}</h2><p>${tr("Choose a format. Inspect part of its real pinned control, then connect it to a saved parser observation.", "Elige un formato. Inspecciona parte de su control fijado y relaciónalo con una observación guardada del parser.")}</p></div><strong>${state.explored.size} / ${state.catalog.demos.length} ${tr("explored", "explorados")}</strong></div>
      <label class="teach-quiz-picker">${tr("FORMAT", "FORMATO")} <select id="teach-quiz-select">${state.catalog.demos.map((item) => `<option value="${escapeHtml(item.format)}" ${item.format === state.quizFormat ? "selected" : ""}>${escapeHtml(state.catalog.formats.find((format) => format.id === item.format)?.label || item.format)}</option>`).join("")}</select></label>
      <div class="teach-quiz-body"><div class="teach-quiz-file"><span class="teach-overline">${escapeHtml(label)} · ${escapeHtml(demo.control.split("/").pop())}</span><div class="teach-quiz-bytes" role="img" aria-label="${tr("Highlighted control bytes at offset", "Bytes destacados del control en la posición")} ${lesson.clueOffset}: hex ${escapeHtml(clueHex)}, ASCII ${escapeHtml(clueAscii)}">${lesson.tokens.map((token, index) => `<span class="teach-byte ${token.focus ? "is-clue" : ""}" style="--n:${index}" aria-hidden="true"><b>${escapeHtml(token.hex)}</b><small>${escapeHtml(token.ascii)}</small></span>`).join("")}</div><p>${tr("Clue starts at byte offset", "La pista empieza en la posición") } <b>${lesson.clueOffset}</b>. <a href="${escapeHtml(localControlUrl(demo))}" target="_blank" rel="noopener noreferrer">${tr("Open control", "Abrir control")} ↗</a></p></div>
      <div class="teach-quiz-answer"><h3>${escapeHtml(lessonCopy.question)}</h3><div class="teach-quiz-choices">${lessonCopy.choices.map((choice, index) => `<button type="button" data-teach-choice="${index}" ${complete ? "disabled" : ""} class="${complete && index === lesson.answer ? "is-correct" : ""}">${escapeHtml(choice)}</button>`).join("")}</div><p id="teach-quiz-feedback" role="status">${complete ? tr("Explanation revealed.", "Explicación revelada.") : tr("Choose an answer or reveal the explanation.", "Elige una respuesta o revela la explicación.")}</p><button type="button" class="teach-quiz-reveal" data-teach-reveal ${complete ? "hidden" : ""}>${tr("Reveal explanation", "Revelar explicación")}</button>${complete ? `<div class="teach-quiz-explanation"><strong>${tr("Saved parser receipt", "Registro guardado del parser")}</strong><p>${escapeHtml(lessonCopy.explanation)}</p><pre>${escapeHtml(JSON.stringify(lesson.output, null, 2))}</pre></div>` : ""}</div></div>`;
  }

  function answerQuiz(index) {
    if (state.explored.has(state.quizFormat)) return;
    const lesson = demoFor(state.quizFormat).lesson;
    if (index === lesson.answer) {
      state.explored.add(state.quizFormat);
      quiz();
    } else {
      el(`[data-teach-choice="${index}"]`).classList.add("is-wrong");
      el("#teach-quiz-feedback").textContent = tr("That field belongs to another format. Try again.", "Ese campo pertenece a otro formato. Inténtalo de nuevo.");
    }
  }

  function wire() {
    el("#teach-form").addEventListener("submit", (event) => {
      event.preventDefault();
      const input = el("#teach-input");
      const command = input.value.trim();
      input.value = "";
      if (!state.busy && command) void execute(command, true);
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
    root.innerHTML = `<p class="teach-loading" role="status">${tr("Loading the pinned control catalog…", "Cargando el catálogo de controles fijados…")}</p>`;
    try {
      const response = await fetch(new URL(`${assetRoot}catalog.json`, document.baseURI));
      if (!response.ok) throw new Error(`catalog HTTP ${response.status}`);
      state.catalog = await response.json();
      state.demos = new Map(state.catalog.demos.map((demo) => [demo.format, demo]));
      if (liveIds.some((id) => !state.demos.has(id)) || state.catalog.demos.some((demo) => !demo.lesson)) throw new Error(tr("catalog is missing a teaching control", "falta un control didáctico en el catálogo"));
      const requested = new URL(location.href).searchParams.get("format");
      const initial = liveIds.includes(requested) ? requested : "png";
      state.quizFormat = requested && state.demos.has(requested) ? requested : initial;
      shell();
      wire();
      quiz();
      terminalLine("welcome", tr("Parsarium browser lab. Type help for commands. Loading a pinned control now…", "Laboratorio de Parsarium. Escribe help para ver los comandos. Cargando un control fijado…"));
      await execute(`load ${initial}`);
    } catch (error) {
      root.innerHTML = `<p class="teach-loading teach-loading-error" role="alert">${tr("The teaching catalog could not be loaded.", "No se pudo cargar el catálogo didáctico.")} ${escapeHtml(error instanceof Error ? error.message : String(error))}</p>`;
    }
  }
  void init();
})();
