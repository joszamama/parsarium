import ar.com.hjg.pngj.ImageInfo;
import ar.com.hjg.pngj.ImageLineHelper;
import ar.com.hjg.pngj.ImageLineInt;
import ar.com.hjg.pngj.PngReader;
import ar.com.hjg.pngj.PngjInputException;
import ar.com.hjg.pngj.PngjUnsupportedException;
import ar.com.hjg.pngj.chunks.PngChunkPLTE;
import ar.com.hjg.pngj.chunks.PngChunkTRNS;
import java.io.ByteArrayInputStream;
import java.nio.file.Files;
import java.nio.file.Path;

public final class PngjHarness {
    record Parsed(int width, int height, String pixels) {}

    // 16-bit samples report their high byte; scaleUp has already widened 1, 2 and 4-bit grey.
    static int sample8(ImageInfo info, int value) {
        return info.bitDepth == 16 ? value >> 8 : value;
    }

    // Straight 8-bit ARGB of one pixel: palette entries and tRNS come from the file's own chunks;
    // tRNS colour keys compare the unscaled samples, as the PNG specification defines them.
    static int argb(ImageInfo info, PngChunkPLTE palette, PngChunkTRNS trns, int[] raw, int[] scaled, int column) {
        int offset = column * info.channels;
        if (info.indexed) {
            int index = raw[offset];
            int[] alphas = trns == null ? null : trns.getPalletteAlpha();
            int alpha = alphas != null && index < alphas.length ? alphas[index] : 255;
            return (alpha << 24) | palette.getEntry(index);
        }
        if (info.greyscale) {
            int gray = sample8(info, scaled[offset]);
            int alpha = info.alpha ? sample8(info, scaled[offset + 1])
                    : trns != null && raw[offset] == trns.getGray() ? 0 : 255;
            return (alpha << 24) | (gray << 16) | (gray << 8) | gray;
        }
        int red = sample8(info, scaled[offset]), green = sample8(info, scaled[offset + 1]);
        int blue = sample8(info, scaled[offset + 2]);
        int alpha;
        if (info.alpha) {
            alpha = sample8(info, scaled[offset + 3]);
        } else {
            int[] key = trns == null ? null : trns.getRGB();
            alpha = key != null && raw[offset] == key[0] && raw[offset + 1] == key[1]
                    && raw[offset + 2] == key[2] ? 0 : 255;
        }
        return (alpha << 24) | (red << 16) | (green << 8) | blue;
    }

    static Parsed parse(byte[] data) {
        if (data.length == 0 || data.length > (1 << 20)) {
            return new Parsed(0, 0, "");
        }
        PngReader reader = new PngReader(new ByteArrayInputStream(data));
        try {
            ImageInfo info = reader.imgInfo;
            int width = info.cols;
            int height = info.rows;
            String pixels = "";
            for (int row = 0; row < height; row++) {
                ImageLineInt line = (ImageLineInt) reader.readRow();
                if (row == 0) {
                    int[] raw = line.getScanline().clone();
                    ImageLineHelper.scaleUp(line);
                    PngChunkPLTE palette = reader.getMetadata().getPLTE();
                    PngChunkTRNS trns = reader.getMetadata().getTRNS();
                    pixels = String.format("%08x", argb(info, palette, trns, raw, line.getScanline(), 0));
                    if (width > 1) {
                        pixels += String.format(",%08x", argb(info, palette, trns, raw, line.getScanline(), 1));
                    }
                }
            }
            reader.end();
            return new Parsed(width, height, pixels);
        } finally {
            reader.close();
        }
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try {
            parse(data);
        } catch (PngjInputException | PngjUnsupportedException ignored) {
            // Documented input rejection is an ordinary fuzz outcome.
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("expected control path");
        Parsed result = parse(Files.readAllBytes(Path.of(args[0])));
        System.out.printf("{\"width\":%d,\"height\":%d,\"pixels\":\"%s\"}%n",
                result.width, result.height, result.pixels);
    }
}
