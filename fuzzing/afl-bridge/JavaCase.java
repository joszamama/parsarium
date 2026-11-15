import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Path;

public final class JavaCase {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("one input path required");
        byte[] data = Files.readAllBytes(Path.of(args[0]));
        String target = System.getenv("PARSARIUM_TARGET_CLASS");
        Method method = Class.forName(target).getMethod("fuzzerTestOneInput", byte[].class);
        method.invoke(null, (Object) data);
    }
}
