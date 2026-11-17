globalThis.parsariumParseLocal = async function parseLocal(input) {
  const context = new OfflineAudioContext(1, 8000, 8000);
  const data = new Uint8Array(input);
  const decoded = await context.decodeAudioData(data.buffer.slice(0));
  return { sampleRate: decoded.sampleRate, channels: decoded.numberOfChannels,
    samples: decoded.length };
};
//# sourceURL=parsarium-browser-harness.js
