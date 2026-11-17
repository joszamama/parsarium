"""The Java TOML night_config_toml path keeps its receipts, overlay and AFL++ feedback consistent."""

import unittest

from tests.test_java_toml_pilot import check_project


class JavaTomlNightConfigTomlTest(unittest.TestCase):
    def test_project_receipts_overlay_and_feedback(self):
        check_project(self, "night_config_toml")


if __name__ == "__main__":
    unittest.main()
