globalThis.parsariumParseLocal = async function parseLocal(input) {
  const context = new OfflineAudioContext(1, 4, 8000);
  const decoded = await context.decodeAudioData(new Uint8Array(input).buffer);
  return { sampleRate: decoded.sampleRate, channels: decoded.numberOfChannels,
    sampleCount: decoded.length,
    sampleSigns: Array.from(decoded.getChannelData(0), (value) => Math.sign(value)) };
};
//# sourceURL=parsarium-browser-harness.js
