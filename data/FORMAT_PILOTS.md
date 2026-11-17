# Pilot format cells

`data/formats.json` lists formats and their phase. The ten active formats continue to
populate `data/cells.json`, `data/parser-readmes.json`, and the top-level totals in
`data/projects-coverage.json`. JSON, XML, plain MP3, and TOML are pilots. Their 32
ecosystem cells live in `data/pilot-cells.json`, their parser guide index lives in
`data/pilot-parser-readmes.json`, and their coverage appears under the `pilot` key
of `data/projects-coverage.json`. Every pilot cell stays explicitly incomplete.
Zero in an unstarted cell means no verified path has been recorded, not that no
parser exists. Plain MP3 does not replace the active MP3-with-ID3v2 format.
DNS (one RFC 1035 wire-format message as local bytes) is also a pilot, with eight
more cells; its scope and controls are in `catalog/dns/PROTOCOL.md`.

## Add a verified pilot path

1. Add `data/<ecosystem>/<format>/cell.json` with a `pilot_*` status, actual counts,
   search bounds, and uncertainty. Add `parsers.json` and/or `standard.json` only
   for verified paths. Keep search leads separate. Third-party records need a
   pinned release, license, documented local input API, parser family, valid
   control, saved result, and numeric adoption signal with provenance. Standard
   API records need official documentation, a control, expected result, and saved
   receipt. A Docker project with a current receipt may be linked from the record.
2. Regenerate and check the separated matrices and guides:

   ```sh
   python3 scripts/build_matrix.py
   python3 scripts/validate_catalog.py
   python3 scripts/audit_projects.py --write
   python3 scripts/build_readmes.py
   python3 scripts/audit_projects.py --check
   python3 scripts/build_readmes.py --check
   python3 parsarium.py list --format json
   ```

   An edit to `parsarium.py` changes the saved CLI hash for the Tkinter standard
   feedback gate. Refresh it with `python3 scripts/verify_standard_feedback.py`
   before the audit and guide checks when that file changes.

3. Review the pilot row and its uncertainty. A verified project raises its pilot
   runnable count only when its parser coverage and feedback receipt pass the
   existing audit gates. Pilot counts never enter the ten-format active totals.

`data/formats.json` is the format-choice source for the CLI and catalog tools. A
new format starts in the pilot phase; moving one to active requires a separate
review of all eight cells and the aggregate consumers, including the website.
