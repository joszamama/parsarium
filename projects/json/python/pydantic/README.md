# pydantic — JSON / Python

`pydantic` 2.14.3 accepts local JSON bytes through the documented [`TypeAdapter[Any].validate_json(data)`](https://docs.pydantic.dev/latest/api/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_json) API. Its pinned `pydantic-core` 2.50.4 dependency invokes Jiter 0.18.0, a Rust JSON parser. The [source lock](source-lock.json) records both source archives and Jiter's Cargo checksum. The adapter returns JSON structure and selected values from the valid object and array controls.

```sh
python3 parsarium.py build json python pydantic
python3 parsarium.py run json python pydantic controls/json/structure.json
python3 parsarium.py afl build json python pydantic
python3 parsarium.py afl prepare json python pydantic runs/json-pydantic-afl
python3 parsarium.py afl run runs/json-pydantic-afl --check
```

The container builds `pydantic-core` from source with Rust LLVM coverage instrumentation. Coverage and AFL feedback must include source regions in Jiter `parse.rs`; Python wrapper line tracing alone does not satisfy this path. The object control covered 420 Jiter source region start lines, including 95 in `parse.rs`. On repeated valid object and array controls, 191 Jiter source features and 191 AFL tuples differed. LLVM export warned about 99 whole-extension functions with mismatched profile data; the receipt uses scoped Jiter regions and makes no claim about complete extension coverage. The two valid controls establish only their tested JSON structures. PyPI Stats downloads measure installation of the whole `pydantic` package, including uses unrelated to JSON parsing.
