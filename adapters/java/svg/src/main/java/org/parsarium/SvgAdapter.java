package org.parsarium;

import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.net.URI;
import java.nio.file.Files;
import java.nio.file.Path;
import javax.imageio.ImageIO;

import org.apache.batik.anim.dom.SAXSVGDocumentFactory;
import org.apache.batik.transcoder.TranscoderInput;
import org.apache.batik.transcoder.TranscoderOutput;
import org.apache.batik.transcoder.image.PNGTranscoder;
import org.apache.batik.util.XMLResourceDescriptor;
import org.w3c.dom.Document;

import com.github.weisj.jsvg.parser.LoaderContext;
import com.github.weisj.jsvg.parser.SVGLoader;
import com.github.weisj.jsvg.view.ViewBox;
import com.kitfox.svg.SVGDiagram;
import com.kitfox.svg.SVGUniverse;

public final class SvgAdapter {
    private SvgAdapter() {}

    public static void main(String[] args) throws Exception {
        if (args.length != 2) throw new IllegalArgumentException("usage: label local.svg");
        Path path = Path.of(args[1]);
        switch (args[0]) {
            case "batik-anim" -> {
                SAXSVGDocumentFactory factory = new SAXSVGDocumentFactory(
                    XMLResourceDescriptor.getXMLParserClassName());
                try (InputStream input = Files.newInputStream(path)) {
                    Document svg = factory.createDocument(path.toUri().toString(), input);
                    int rects = svg.getDocumentElement()
                        .getElementsByTagNameNS("http://www.w3.org/2000/svg", "rect").getLength();
                    String width = svg.getDocumentElement().getAttribute("width");
                    String height = svg.getDocumentElement().getAttribute("height");
                    System.out.printf("{\"width\":%s,\"height\":%s,\"rects\":%d}%n",
                        width, height, rects);
                }
            }
            case "batik-transcoder" -> {
                PNGTranscoder parser = new PNGTranscoder();
                ByteArrayOutputStream bytes = new ByteArrayOutputStream();
                try (InputStream input = Files.newInputStream(path)) {
                    parser.transcode(new TranscoderInput(input), new TranscoderOutput(bytes));
                }
                printPixels(ImageIO.read(new java.io.ByteArrayInputStream(bytes.toByteArray())));
            }
            case "jsvg" -> {
                com.github.weisj.jsvg.SVGDocument svg;
                try (InputStream input = Files.newInputStream(path)) {
                    svg = new SVGLoader().load(input, path.toUri(), LoaderContext.createDefault());
                }
                if (svg == null) throw new IllegalStateException("JSVG did not parse SVG");
                BufferedImage image = new BufferedImage(2, 1, BufferedImage.TYPE_INT_ARGB);
                Graphics2D graphics = image.createGraphics();
                svg.render(null, graphics, new ViewBox(0, 0, 2, 1));
                graphics.dispose();
                printPixels(image);
            }
            case "svg-salamander" -> {
                SVGUniverse universe = new SVGUniverse();
                URI uri;
                try (InputStream input = Files.newInputStream(path)) {
                    uri = universe.loadSVG(input, "parsarium-control.svg");
                }
                SVGDiagram svg = universe.getDiagram(uri);
                if (svg == null) throw new IllegalStateException("Salamander did not parse SVG");
                BufferedImage image = new BufferedImage(2, 1, BufferedImage.TYPE_INT_ARGB);
                Graphics2D graphics = image.createGraphics();
                svg.render(graphics);
                graphics.dispose();
                printPixels(image);
            }
            default -> throw new IllegalArgumentException("unknown adapter: " + args[0]);
        }
    }

    private static void printPixels(BufferedImage image) {
        System.out.printf("{\"width\":%d,\"height\":%d,\"pixels\":\"%08x,%08x\"}%n",
            image.getWidth(), image.getHeight(), image.getRGB(0, 0), image.getRGB(1, 0));
    }
}
