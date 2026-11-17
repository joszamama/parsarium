// Documented Buffer API with cbrEstimate=false: mp3-duration walks MPEG
// frame headers and sums samples/sampleRate, then rounds to milliseconds.
import duration from 'mp3-duration';

export async function parse(bytes) {
  const seconds = await duration(bytes, false);
  if (!Number.isFinite(seconds) || seconds <= 0)
    throw new Error('no MPEG audio duration returned');
  return { duration_ms: Math.round(seconds * 1000) };
}
