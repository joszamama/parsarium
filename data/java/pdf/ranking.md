# Java × PDF: verified parser ranking

20 verified third-party package paths; working goal 20, original ceiling 30. The metric is deps.dev's version-level public direct dependent count, captured at 2026-11-12T04:45:54.000486+00:00. This is a known-public-dependents proxy for adoption of each exact release, not downloads; coverage and version age may bias it. It is compared only within Java. 1 package(s) lack a metric and remain unranked.

Search hits, unresolved leads, and JDK APIs are separate from this ranking. See `cell.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Direct dependents | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [pdfbox](https://javadoc.io/static/org.apache.pdfbox/pdfbox/3.0.8/org/apache/pdfbox/Loader.html) | org.apache.pdfbox:pdfbox:3.0.8 | 119 | PDF page count | Apache PDFBox |
| 2 | [itextpdf](https://javadoc.io/static/com.itextpdf/itextpdf/5.5.13/com/itextpdf/text/pdf/PdfReader.html) | com.itextpdf:itextpdf:5.5.13 | 80 | PDF page count | iText 5 PDF reader |
| 3 | [openpdf](https://javadoc.io/static/com.github.librepdf/openpdf/3.0.5/com.github.librepdf.openpdf/org/openpdf/text/pdf/PdfReader.html) | com.github.librepdf:openpdf:3.0.5 | 29 | PDF page count | OpenPDF PDF reader (iText lineage) |
| 4 | [itext-kernel](https://repo.maven.apache.org/maven2/com/itextpdf/kernel/9.8.0/kernel-9.8.0-javadoc.jar) | com.itextpdf:kernel:9.8.0 | 11 | PDF page count | iText 7/9 kernel PDF reader |
| 5 | [swinglabs-pdf-renderer](https://javadoc.io/static/org.swinglabs/pdf-renderer/1.0.5/com/sun/pdfview/PDFFile.html) | org.swinglabs:pdf-renderer:1.0.5 | 9 | PDF page count | Sun PDF Renderer |
| 5 | [verapdf-parser](https://repo.maven.apache.org/maven2/org/verapdf/parser/1.30.4/parser-1.30.4-javadoc.jar) | org.verapdf:parser:1.30.4 | 9 | PDF page count | veraPDF parser |
| 7 | [icepdf-core](https://javadoc.io/static/org.icepdf.os/icepdf-core/6.2.2/org/icepdf/core/pobjects/Document.html) | org.icepdf.os:icepdf-core:6.2.2 | 5 | PDF page count | ICEpdf 6 core |
| 7 | [tess4j-pdfbox](https://github.com/nguyenq/tess4j/blob/master/src/main/java/net/sourceforge/tess4j/util/PdfBoxUtilities.java) | net.sourceforge.tess4j:tess4j:5.20.0 | 5 | PDF page count | Tess4J PDF utility over PDFBox |
| 9 | [pdfbox-preflight](https://javadoc.io/static/org.apache.pdfbox/preflight/3.0.8/org/apache/pdfbox/preflight/parser/PreflightParser.html) | org.apache.pdfbox:preflight:3.0.8 | 4 | PDF page count | Apache PDFBox Preflight wrapper |
| 10 | [openpdf-renderer](https://github.com/LibrePDF/OpenPDF/blob/master/openpdf-renderer/src/main/java/org/openpdf/renderer/PDFFile.java) | com.github.librepdf:openpdf-renderer:3.0.5 | 3 | PDF page count | OpenPDF renderer (Sun PDF Renderer lineage) |
| 11 | [icepdf8](https://repo.maven.apache.org/maven2/com/github/pcorless/icepdf/icepdf-core/8.0.0/icepdf-core-8.0.0-javadoc.jar) | com.github.pcorless.icepdf:icepdf-core:8.0.0 | 2 | PDF page count | ICEpdf 8 community fork |
| 11 | [jpdfium](https://github.com/Stirling-Tools/JPDFium) | com.stirling:jpdfium:1.3.1 | 2 | PDF page count | PDFium native engine via JPDFium FFM |
| 11 | [sambox](https://github.com/torakiki/sambox) | org.sejda:sambox:4.0.0.M8 | 2 | PDF page count | SAMBox (PDFBox fork) |
| 11 | [tika-pdf](https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-pdf-module/4.2.0/tika-parser-pdf-module-4.2.0-javadoc.jar) | org.apache.tika:tika-parser-pdf-module:4.2.0 | 2 | PDF page count | Apache Tika PDF module over PDFBox |
| 15 | [jpod-original](https://repo.maven.apache.org/maven2/de/intarsys/opensource/jPod/5.6/jPod-5.6-javadoc.jar) | de.intarsys.opensource:jPod:5.6 | 1 | PDF page count | jPod PDF parser (original) |
| 15 | [pdfviewfx](https://github.com/dlsc-software-consulting-gmbh/PDFViewFX/blob/master/pdfviewfx/src/main/java/com/dlsc/pdfviewfx/PDFBoxDocument.java) | com.dlsc.pdfviewfx:pdfviewfx:3.6.1 | 1 | PDF page count | PDFViewFX over PDFBox |
| 17 | [pdfium4j](https://github.com/grimmory-tools/PDFium4j) | org.grimmory:pdfium4j:1.3.0 | 0 | PDF page count | PDFium native engine via PDFium4j FFM |
| 17 | [pdfjet](https://github.com/edragoev1/pdfjet) | com.pdfjet:pdfjet:9.1.7 | 0 | PDF page count | PDFjet reader |
| 17 | [scireum-jpod](https://repo.maven.apache.org/maven2/com/scireum/jpod/2.0/jpod-2.0-javadoc.jar) | com.scireum:jpod:2.0 | 0 | PDF page count | jPod PDF parser (Scireum fork) |
| unranked | [pdfclown](https://pdfclown.org/overview/features/) | official SourceForge release 0.1.2-Beta | unknown | PDF page count | PDF Clown parser |
