# Parsson — JSON / Java

Pinned `org.eclipse.parsson:parsson:1.1.9` implements Jakarta JSON-P with its own `JsonParserImpl` and `JsonTokenizer`. The `jakarta.json-api:2.1.3` dependency supplies interfaces and value types. [Manifest](manifest.json) · [source lock](source-lock.json) · [verification receipt](verification.json).

The adapter reads a local `InputStream` with `JsonProviderImpl.createParser`, obtains a `JsonValue`, and calls `hasNext()` after the root to check EOF. It prints an observable structural summary. The two controls cover valid nested object and array documents, not the full JSON grammar. [API and family evidence](../../../../catalog/json/java/parsson/README.md).

```sh
python3 parsarium.py build json java parsson
python3 parsarium.py run json java parsson controls/json/nested-object.json
python3 parsarium.py replay json java parsson CORPUS_DIR runs/json-parsson-replay
python3 parsarium.py afl build json java parsson
python3 parsarium.py afl prepare json java parsson runs/json-parsson-afl
```

`afl prepare` seeds a run; it does not start a campaign.
