# GNOME Papers (PDF / C)

This harness calls Papers 51.1 `pps_document_factory_get_document` and `pps_document_load` with a local PDF URI, then reports `pps_document_get_n_pages`. The Papers PDF backend uses Poppler GLib 26.11.0 and the same Poppler PDF core as Evince and poppler-glib. They are distinct public API paths over one parser family.

```sh
python3 parsarium.py run pdf c gnome-papers controls/pdf/two-page.pdf
python3 parsarium.py afl build pdf c gnome-papers
python3 parsarium.py afl prepare pdf c gnome-papers /tmp/papers-afl
python3 parsarium.py afl run /tmp/papers-afl --check
```

The control result is `{"pages":2}`. `controls/pdf/one-page.pdf` is a second valid case with `{"pages":1}`. Docker builds the pinned Papers and Poppler sources with LLVM line coverage; the AFL++ overlay instruments the Papers PDF backend and Poppler parser sources. AFL's target is a one-shot file replay (`/work/replay @@`). The harness copies supplied bytes to a local temporary PDF because the documented Papers API accepts a URI.

The valid control covers 145 Papers PDF backend lines and 1,272 Poppler core lines. AFL++ records 348 PDF parser edges, with identical maps across three control repeats and stable differences for the valid one-page case. `--check` inspects the prepared command without starting a campaign.

`verification.json` and the AFL overlay receipt record exact source and image hashes, observed output, coverage, and input-sensitive feedback. The source lock pins Papers 51.1 and Poppler 26.11.0. This project does not run a fuzz campaign.
