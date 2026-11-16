globalThis.parsariumParseLocal = async function parseLocal(input) {
  const blob = new Blob([new Uint8Array(input)], { type: 'image/svg+xml' });
  const url = URL.createObjectURL(blob);
  const image = new Image();
  try {
    image.src = url;
    await image.decode();
    const canvas = document.createElement('canvas');
    canvas.width = image.naturalWidth;
    canvas.height = image.naturalHeight;
    const context = canvas.getContext('2d');
    context.drawImage(image, 0, 0);
    return { width: image.naturalWidth, height: image.naturalHeight,
      rgba: Array.from(context.getImageData(0, 0, image.naturalWidth, image.naturalHeight).data) };
  } finally { URL.revokeObjectURL(url); }
};
//# sourceURL=parsarium-browser-harness.js
