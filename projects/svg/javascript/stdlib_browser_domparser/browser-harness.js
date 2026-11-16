globalThis.parsariumParseLocal = async function parseLocal(input) {
  const source = new TextDecoder().decode(new Uint8Array(input));
  const document = new DOMParser().parseFromString(source, 'image/svg+xml');
  const root = document.documentElement;
  if (!(root instanceof SVGSVGElement)) throw new Error('not an SVG root');
  const rects = [...root.querySelectorAll('rect')];
  return { width: root.width.baseVal.value, height: root.height.baseVal.value,
    rects: rects.length, fills: rects.map((rect) => rect.getAttribute('fill')),
    typed_root: root instanceof SVGSVGElement,
    typed_rects: rects.every((rect) => rect instanceof SVGRectElement) };
};
//# sourceURL=parsarium-browser-harness.js
