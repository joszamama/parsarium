"""The Java TOML jackson_dataformat_toml path keeps its receipts, overlay and AFL++ feedback consistent."""

import unittest

from tests.test_java_toml_pilot import check_project


class JavaTomlJacksonDataformatTomlTest(unittest.TestCase):
    def test_project_receipts_overlay_and_feedback(self):
        check_project(self, "jackson_dataformat_toml")


if __name__ == "__main__":
    unittest.main()
