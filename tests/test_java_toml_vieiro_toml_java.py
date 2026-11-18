"""The Java TOML toml-java (vieiro) path keeps its receipts, overlay and AFL++ feedback consistent."""

import unittest

from tests.test_java_toml_pilot import check_project


class JavaTomlVieiroTomlJavaTest(unittest.TestCase):
    def test_project_receipts_overlay_and_feedback(self):
        check_project(self, "vieiro_toml_java")


if __name__ == "__main__":
    unittest.main()
