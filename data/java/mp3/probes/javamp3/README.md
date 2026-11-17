# JavaMP3 1.0.1 eligibility probe

The [project documentation](https://github.com/delthas/JavaMP3) shows `new Sound(new BufferedInputStream(Files.newInputStream(path)))`, followed by `Sound.read(byte[])` for signed 16-bit PCM, `getSamplingFrequency()`, and `isStereo()`. The Maven `fr.delthas:javamp3:1.0.1` release is MIT licensed. Its POM has no runtime dependency; its source JAR contains `Sound.java` and `Decoder.java` and no JavaZoom or JLayer package reference. This does not establish complete code ancestry.

The pinned [probe](Probe.java) uses exactly that local stream API. [run.py](run.py) downloads the release JAR, sources JAR, and POM from Maven Central, verifies their SHA-256 hashes, and runs the probe in a pinned arm64 Temurin image. It checks the decoded PCM sample count against the repository's independent MPEG frame walker. The two inputs are the existing valid, untagged Layer III controls; this is an eligibility check, not a malformed-input or fuzzing experiment.

With Python 3, `curl`, Docker, and arm64 image support:

```sh
python3 data/java/mp3/probes/javamp3/run.py --check
```

The recorded [result](result.json) is exact for the 44.1 kHz mono control: 44,100 Hz, one channel, 25,344 PCM bytes and 12,672 samples. Construction of `Sound` for the valid 22.05 kHz stereo control throws `ArrayIndexOutOfBoundsException: Index 2304 out of bounds for length 2304` at `Decoder.samples_III(Decoder.java:773)`. The independent control oracle expects 22,050 Hz, two channels, and 6,912 decoded samples. This release therefore fails the two-control selection gate. There is no selected parser harness, JaCoCo receipt, or AFL++ feedback claim for this lead.
