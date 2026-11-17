globalThis.parsariumParsePngBlob = async function parsePngBlob(input) {
  const blob = new Blob([new Uint8Array(input)], { type: 'image/png' });
  const bitmap = await createImageBitmap(blob);
  try {
    const canvas = document.createElement('canvas');
    canvas.width = bitmap.width;
    canvas.height = bitmap.height;
    const context = canvas.getContext('2d');
    context.drawImage(bitmap, 0, 0);
    return {
      width: bitmap.width,
      height: bitmap.height,
      rgba: Array.from(context.getImageData(0, 0, bitmap.width, bitmap.height).data)
    };
  } finally {
    bitmap.close();
  }
};
//# sourceURL=parsarium-browser-harness.js
