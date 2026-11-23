import java.awt.Image;
import java.awt.Toolkit;
import java.awt.image.BufferedImage;
import java.awt.image.PixelGrabber;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Iterator;
import javax.imageio.ImageIO;
import javax.imageio.ImageReader;
import javax.imageio.stream.ImageInputStream;
import javax.swing.ImageIcon;
import javax.sound.sampled.AudioFileFormat;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;

public final class GenericHarness {
    private static final String MODE = "toolkit";
    private static final String SUFFIX = ".png";

    // A one-pixel-wide image has no second pixel; report the first only.
    private static String pixels(int width, int height, int first, int second) {
        String values = width > 1 ? String.format("%08x,%08x", first, second) : String.format("%08x", first);
        return String.format("{\"width\":%d,\"height\":%d,\"pixels\":\"%s\"}", width, height, values);
    }

    private static String imageResult(BufferedImage image) throws Exception {
        if (image == null) throw new IllegalArgumentException("no decoded PNG pixels");
        return pixels(image.getWidth(), image.getHeight(),
                      image.getRGB(0, 0), image.getWidth() > 1 ? image.getRGB(1, 0) : 0);
    }

    private static String imageResult(Image image) throws Exception {
        if (image == null) throw new IllegalArgumentException("no decoded PNG image");
        int[] argb = new int[2];
        PixelGrabber grabber = new PixelGrabber(image, 0, 0, 2, 1, argb, 0, 2);
        if (!grabber.grabPixels(3000)) throw new IllegalArgumentException("PNG pixel decode timed out");
        int width = image.getWidth(null), height = image.getHeight(null);
        if (width < 1 || height < 1) throw new IllegalArgumentException("no decoded PNG pixels");
        return pixels(width, height, argb[0], argb[1]);
    }

    private static String parse(byte[] data) throws Exception {
        if (data.length == 0 || data.length > (1 << 20)) return "";
        Path file = Files.createTempFile("parsarium-jdk-", SUFFIX);
        try {
            Files.write(file, data);
            switch (MODE) {
                case "imageio": return imageResult(ImageIO.read(file.toFile()));
                case "imagereader": {
                    Iterator<ImageReader> readers = ImageIO.getImageReadersByFormatName("PNG");
                    if (!readers.hasNext()) throw new IllegalStateException("no JDK PNG reader");
                    ImageReader reader = readers.next();
                    try (ImageInputStream input = ImageIO.createImageInputStream(new ByteArrayInputStream(data))) {
                        reader.setInput(input);
                        return imageResult(reader.read(0));
                    } finally { reader.dispose(); }
                }
                case "imageicon": return imageResult(new ImageIcon(data).getImage());
                case "toolkit": return imageResult(new ImageIcon(Toolkit.getDefaultToolkit().createImage(data)).getImage());
                case "audio_file_format": {
                    AudioFileFormat parsed = AudioSystem.getAudioFileFormat(file.toFile());
                    return String.format("{\"type\":\"%s\",\"sample_rate\":%d,\"channels\":%d,\"frames\":%d}",
                        parsed.getType(), (int) parsed.getFormat().getSampleRate(),
                        parsed.getFormat().getChannels(), parsed.getFrameLength());
                }
                case "audio_input_stream": {
                    try (AudioInputStream parsed = AudioSystem.getAudioInputStream(file.toFile())) {
                        int sampleBytes = parsed.readNBytes(8).length;
                        return String.format("{\"sample_rate\":%d,\"channels\":%d,\"frames\":%d,\"sample_bytes\":%d}",
                            (int) parsed.getFormat().getSampleRate(),
                            parsed.getFormat().getChannels(), parsed.getFrameLength(), sampleBytes);
                    }
                }
                default: throw new IllegalStateException(MODE);
            }
        } finally { Files.deleteIfExists(file); }
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); }
        catch (RuntimeException error) { throw error; }
        catch (Exception ignored) { }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("one input path required");
        System.out.println(parse(Files.readAllBytes(Path.of(args[0]))));
    }
}
