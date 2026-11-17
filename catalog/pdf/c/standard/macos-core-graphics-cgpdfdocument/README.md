# macOS Core Graphics CGPDFDocument — PDF / C

- **Runtime:** ISO/IEC 9899:2024 C standard library and macOS Core Graphics platform runtime
- **Input API:** `CFURLCreateFromFileSystemRepresentation(local path); CGPDFDocumentCreateWithURL(CFURLRef); CGPDFDocumentGetNumberOfPages`
- **Official documentation:** [reference](https://developer.apple.com/documentation/coregraphics/cgpdfdocument/init%28_%3A%29-2gtsd?language=objc)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../../controls/pdf/one-page.pdf)
- **Inventory and verification:** [standard API record](../../../../../data/c/pdf/standard.json) · [saved result](../../../../../data/c/pdf/verification.json)

**Parser family:** Apple Core Graphics PDF parser

## Observed control result

```json
{
  "pages": 1
}
```

[Control adapter](../../../../../adapters/c/pdf/coregraphics.c)

## Run this macOS control

[Host harness and control receipt](../../../../../projects/pdf/c/stdlib_coregraphics/README.md)

```sh
python3 projects/pdf/c/stdlib_coregraphics/verify-control.py
```

Core Graphics runs on macOS. Its parser source and AFL++ feedback are unavailable, so this path remains staged.
