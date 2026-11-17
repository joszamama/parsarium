// Local bytes reach mediabunny's documented Input(BufferSource) MP3 demuxer and packet sink.
import { ALL_FORMATS, BufferSource, EncodedPacketSink, Input } from 'mediabunny';

export async function parse(bytes) {
  const input = new Input({ source: new BufferSource(bytes), formats: ALL_FORMATS });
  try {
    const format = await input.getFormat();
    const track = await input.getPrimaryAudioTrack();
    if (!track) throw new Error('no audio track');
    let frames = 0;
    let frameBytes = 0;
    for await (const packet of new EncodedPacketSink(track).packets()) {
      frames++;
      frameBytes += packet.byteLength;
    }
    const duration = await track.computeDuration();
    return {
      format: format.name,
      codec: track.codec,
      sample_rate: track.sampleRate,
      channels: track.numberOfChannels,
      frames,
      frame_bytes: frameBytes,
      samples_per_channel: Math.round(duration * track.sampleRate),
    };
  } finally {
    input.dispose();
  }
}
