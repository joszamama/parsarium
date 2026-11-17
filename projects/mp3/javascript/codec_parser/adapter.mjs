// Local bytes reach codec-parser's documented CodecParser('audio/mpeg').parseAll(Uint8Array) frame parser.
import CodecParser from 'codec-parser';

export function parse(bytes) {
  let codecHeader = null;
  const parser = new CodecParser('audio/mpeg', { onCodecHeader: header => { codecHeader = header; } });
  const frames = parser.parseAll(new Uint8Array(bytes.buffer, bytes.byteOffset, bytes.byteLength));
  if (frames.length === 0) throw new Error('no MPEG audio frames');
  const first = frames[0];
  const last = frames[frames.length - 1];
  const variants = new Set(frames.map(frame =>
    `${frame.header.layer}|${frame.header.sampleRate}|${frame.header.channels}|${frame.samples}`));
  return {
    codec: parser.codec,
    layer: first.header.layer,
    sample_rate: first.header.sampleRate,
    channels: first.header.channels,
    // parseAll rewrites frame.header.bitrate from frame size; the codec header keeps the table value.
    bitrate: codecHeader ? codecHeader.bitrate * 1000 : null,
    frames: frames.length,
    frame_bytes: frames.reduce((sum, frame) => sum + frame.data.length, 0),
    samples_per_frame: first.samples,
    total_samples: last.totalSamples + last.samples,
    header_variants: variants.size,
  };
}
