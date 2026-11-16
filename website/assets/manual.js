(() => {
  const es = document.body.dataset.lang === "es";
  const store = window.parsariumStore;
  const slug = document.querySelector("article[data-slug]")?.dataset.slug;
  if (!slug || !store) return;

  // Quiz: one attempt counts per question; the best score is remembered.
  const quiz = document.querySelector(".quiz");
  if (quiz) {
    const qs = [...quiz.querySelectorAll(".q")];
    let answered = 0, correct = 0;
    const score = document.createElement("div");
    score.className = "quiz-score";
    score.hidden = true;
    const best = store.get(`quiz:${slug}`);
    qs.forEach((q, n) => {
      q.querySelector(".q-text").dataset.n = String(n + 1).padStart(2, "0");
      const answer = Number(q.dataset.answer);
      const items = [...q.querySelectorAll(".q-opts li")];
      items.forEach((li, k) => {
        const b = document.createElement("button");
        b.type = "button";
        b.innerHTML = li.innerHTML;
        li.replaceChildren(b);
        b.addEventListener("click", () => {
          if (q.classList.contains("done")) return;
          const ok = k === answer;
          b.classList.add(ok ? "right" : "wrong");
          items[answer].firstChild.classList.add("right");
          q.classList.add("done");
          if (!ok) q.classList.add("missed");
          answered++; if (ok) correct++;
          if (answered === qs.length) finish();
        });
      });
    });
    const finish = () => {
      const previous = store.get(`quiz:${slug}`);
      const prevScore = previous ? Number(previous.split("/")[0]) : -1;
      if (correct > prevScore) store.set(`quiz:${slug}`, `${correct}/${qs.length}`);
      score.hidden = false;
      score.innerHTML = `<span><b>${correct}/${qs.length}</b>${es ? (correct === qs.length ? "Todo correcto." : "Lee las explicaciones de las que fallaste.") : (correct === qs.length ? "All correct." : "Read the explanations for the ones you missed.")}</span><button type="button">${es ? "Repetir" : "Try again"}</button>`;
      score.querySelector("button").addEventListener("click", () => {
        answered = 0; correct = 0; score.hidden = true;
        qs.forEach((q) => { q.classList.remove("done", "missed"); q.querySelectorAll("button").forEach((b) => b.classList.remove("right", "wrong")); });
        qs[0].scrollIntoView({ behavior: "smooth", block: "center" });
      });
      window.parsariumProgress();
    };
    quiz.append(score);
    if (best) {
      const note = quiz.querySelector(".section-title .label");
      if (note) note.textContent += es ? ` · tu mejor resultado: ${best}` : ` · your best: ${best}`;
    }
  }

  // Exercises: a done toggle per exercise.
  document.querySelectorAll(".exercises .exercise").forEach((ex, i) => {
    const key = `ex:${slug}:${i + 1}`;
    const b = document.createElement("button");
    b.type = "button";
    b.className = "ex-done";
    const sync = () => {
      const on = store.get(key) === "1";
      b.setAttribute("aria-pressed", String(on));
      b.textContent = on ? (es ? "Hecho ✓" : "Done ✓") : (es ? "Marcar como hecho" : "Mark as done");
      ex.classList.toggle("is-done", on);
    };
    b.addEventListener("click", () => { store.set(key, store.get(key) === "1" ? "0" : "1"); sync(); window.parsariumProgress(); });
    ex.append(b);
    sync();
  });
})();

(async () => {
  document.querySelectorAll(".prose pre").forEach((pre) => window.parsariumCopy && window.parsariumCopy(pre));
  const box = document.querySelector(".inspector[data-manual]");
  if (!box) return;
  const es = document.body.dataset.lang === "es";
  const T = es
    ? { observed: "Lo que devolvió el parser", run: "Para reproducirlo:", right: "Correcto.", wrong: "No exactamente.", bytes: "bytes", of: "de" }
    : { observed: "What the parser reported", run: "To reproduce it:", right: "Right.", wrong: "Not quite.", bytes: "bytes", of: "of" };
  const ECO = { c: "C", cpp: "C++", go: "Go", java: "Java", javascript: "JavaScript", python: "Python", rust: "Rust", php: "PHP" };
  const LABEL = { png: "PNG", zip: "ZIP", mp4: "MP4", wav: "WAV", pdf: "PDF", svg: "SVG", http11: "HTTP/1.1", ascii_ply: "PLY", ascii_pnm: "PNM", mp3_id3v2: "ID3v2" };
  const { demos } = await fetch(box.dataset.manual).then((r) => r.json());
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  box.innerHTML = `<div class="insp-tabs" role="tablist">${demos.map((d, i) =>
    `<button role="tab" data-i="${i}" aria-selected="${i === 0}">${LABEL[d.format] || d.format}</button>`).join("")}</div><div class="insp-body"></div>`;
  const body = box.querySelector(".insp-body");

  const dump = (hex, clue, length) => {
    const bytes = hex.match(/../g) || [];
    // Show the rows around the clue, at most 12 rows.
    const firstRow = Math.max(0, Math.floor(clue / 16) - 4);
    const lastRow = Math.min(Math.ceil(bytes.length / 16), firstRow + 12);
    const rows = [];
    for (let r = firstRow; r < lastRow; r++) {
      const cells = [], chars = [];
      for (let i = r * 16; i < Math.min(bytes.length, r * 16 + 16); i++) {
        const hit = i >= clue && i < clue + length ? " hit" : "";
        const n = parseInt(bytes[i], 16);
        cells.push(`<span class="b${hit}">${bytes[i]}</span>`);
        chars.push(`<span class="${hit.trim()}">${n >= 32 && n < 127 ? esc(String.fromCharCode(n)) : "·"}</span>`);
      }
      rows.push(`<div class="hx-row"><span class="hx-off">${(r * 16).toString(16).padStart(8, "0")}</span><span class="hx-bytes">${cells.join("")}</span><span class="hx-ascii">${chars.join("")}</span></div>`);
    }
    return rows.join("");
  };

  const show = (i) => {
    const d = demos[i];
    const l = es ? { ...d.lesson, ...d.lesson.es } : d.lesson;
    box.querySelectorAll(".insp-tabs button").forEach((b) => b.setAttribute("aria-selected", String(Number(b.dataset.i) === i)));
    body.innerHTML = `<p class="insp-meta">${esc(d.control)} · ${d.bytes} ${T.bytes} · ${esc(d.package)} ${esc(d.release)} (${ECO[d.ecosystem]})</p>
      <div class="insp-dump">${dump(d.hex, l.clueOffset, l.clueLength)}</div>
      <p class="insp-q">${esc(l.question)}</p>
      <div class="insp-choices">${l.choices.map((c, k) => `<button type="button" data-k="${k}">${esc(c)}</button>`).join("")}</div>
      <div class="insp-answer" hidden></div>`;
    const answer = body.querySelector(".insp-answer");
    body.querySelector(".insp-choices").addEventListener("click", (event) => {
      const b = event.target.closest("button"); if (!b) return;
      const k = Number(b.dataset.k);
      b.classList.add(k === l.answer ? "right" : "wrong");
      if (k !== l.answer) return;
      body.querySelector(".insp-dump").classList.add("revealed");
      answer.hidden = false;
      answer.innerHTML = `<p><b>${T.right}</b> ${esc(l.explanation)}</p>
        <p class="label" style="margin-top:12px">${T.observed}</p><pre>${esc(JSON.stringify(l.output, null, 2))}</pre>
        <p class="label">${T.run}</p><pre>${esc(d.controlCommand)}</pre>`;
      answer.querySelectorAll("pre").forEach((pre) => window.parsariumCopy && window.parsariumCopy(pre));
    });
  };
  box.querySelector(".insp-tabs").addEventListener("click", (event) => {
    const b = event.target.closest("button"); if (b) show(Number(b.dataset.i));
  });
  show(0);
})();
