globalThis.parsariumParseLocal = async function parseLocal(input) {
  const blob = new Blob([new Uint8Array(input)], { type: 'video/mp4' });
  const url = URL.createObjectURL(blob);
  const element = document.createElement('video');
  element.preload = 'metadata';
  try {
    await new Promise((resolve, reject) => {
      const timeout = setTimeout(() => reject(new Error('video metadata timeout')), 10000);
      element.addEventListener('loadedmetadata', () => { clearTimeout(timeout); resolve(); }, { once: true });
      element.addEventListener('error', () => { clearTimeout(timeout); reject(new Error(String(element.error?.message))); }, { once: true });
      element.src = url;
    });
    return { width: element.videoWidth, height: element.videoHeight,
      duration: element.duration };
  } finally {
    element.removeAttribute('src');
    element.load();
    URL.revokeObjectURL(url);
  }
};
//# sourceURL=parsarium-browser-harness.js
