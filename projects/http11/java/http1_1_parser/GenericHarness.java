import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.lang.reflect.InvocationTargetException;
import java.nio.file.Files;
import java.nio.file.Path;

public final class GenericHarness {
    private static final String ADAPTER = "org.parsarium.Http11Adapter";
    private static final String LABEL = "webpieces";
    private static final String SUFFIX = ".http";

    private static String parse(byte[] data) throws Exception {
        if (data.length == 0 || data.length > (1 << 20)) return "";
        Path input = Files.createTempFile("parsarium-java-", SUFFIX);
        PrintStream original = System.out;
        ByteArrayOutputStream output = new ByteArrayOutputStream();
        try {
            Files.write(input, data);
            System.setOut(new PrintStream(output, true, "UTF-8"));
            try {
                Class.forName(ADAPTER).getMethod("main", String[].class)
                     .invoke(null, (Object) new String[]{LABEL, input.toString()});
            } catch (InvocationTargetException error) {
                Throwable cause = error.getCause();
                if (cause instanceof Exception checked) throw checked;
                if (cause instanceof Error failure) throw failure;
                throw error;
            }
        } finally {
            System.setOut(original);
            Files.deleteIfExists(input);
        }
        String[] lines = output.toString("UTF-8").trim().split("\r?\n");
        return lines[lines.length - 1];
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
