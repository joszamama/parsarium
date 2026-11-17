"""The Java TOML jtoml path keeps its receipts, overlay and AFL++ feedback consistent."""

import unittest

from tests.test_java_toml_pilot import check_project


class JavaTomlJtomlTest(unittest.TestCase):
    def test_project_receipts_overlay_and_feedback(self):
        check_project(self, "jtoml")


if __name__ == "__main__":
    unittest.main()
