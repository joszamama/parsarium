# php-ziparchive — ZIP / PHP

- **Runtime:** PHP 8.5.12 CLI with zip extension 1.22.8 (libzip 1.12.1) and Phar extension
- **Input API:** `ZipArchive::open(local path, RDONLY); numFiles; getNameIndex; getFromIndex`
- **Official documentation:** [reference](https://www.php.net/manual/en/ziparchive.open.php)
- **Valid control:** [`controls/zip/hello.zip`](../../../../../controls/zip/hello.zip)
- **Inventory and verification:** [standard API record](../../../../../data/php/zip/standard.json) · [saved result](../../../../../data/php/zip/verification.json)

**Parser family:** PHP Zip extension over libzip

## Observed control result

```json
{
  "entries": 1,
  "name": "hello.txt",
  "content": "parsarium\n"
}
```

[Control adapter](../../../../../adapters/php/zip/runtime_ziparchive.php)

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
