import ar.com.hjg.pngj.ImageLineInt;
import ar.com.hjg.pngj.PngReader;
import ar.com.hjg.pngj.PngjInputException;
import ar.com.hjg.pngj.PngjUnsupportedException;
import java.io.ByteArrayInputStream;
import java.nio.file.Files;
import java.nio.file.Path;

public final class PngjHarness {
    record Parsed(int width, int height, String pixels) {}

    static Parsed parse(byte[] data) {
        if (data.length == 0 || data.length > (1 << 20)) {
            return new Parsed(0, 0, "");
        }
        PngReader reader = new PngReader(new ByteArrayInputStream(data));
        try {
            int width = reader.imgInfo.cols;
            int height = reader.imgInfo.rows;
            if (width < 1 || height < 1 || width > 4096 || height > 4096) {
                return new Parsed(width, height, "");
            }
            String pixels = "";
            for (int row = 0; row < height; row++) {
                int[] values = ((ImageLineInt) reader.readRow()).getScanline();
                if (row == 0 && values.length >= 8 && reader.imgInfo.channels == 4) {
                    int first = (values[3] << 24) | (values[0] << 16) | (values[1] << 8) | values[2];
                    int second = (values[7] << 24) | (values[4] << 16) | (values[5] << 8) | values[6];
                    pixels = String.format("%08x,%08x", first, second);
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
