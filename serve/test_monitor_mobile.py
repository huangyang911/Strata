"""Static contracts for Strata's mobile monitor layout."""
from pathlib import Path
import re
import unittest


WEB = Path(__file__).with_name("web")
APP_JS = (WEB / "app.js").read_text(encoding="utf-8")
APP_CSS = (WEB / "app.css").read_text(encoding="utf-8")
INDEX = (WEB / "index.html").read_text(encoding="utf-8")


class MobileMonitorContracts(unittest.TestCase):
    def test_optional_images_tab_does_not_force_mobile_navigation_overflow(self):
        mobile = APP_CSS.split("@media (max-width: 640px)", 1)[1].split("@media (max-width: 360px)", 1)[0]
        self.assertRegex(mobile, r"\.st-header__spacer\s*\{[^}]*display\s*:\s*none")
        self.assertRegex(mobile, r"\.st-header\s+\.st-tabs\s*\{[^}]*flex\s*:\s*1")
        self.assertRegex(mobile, r"\.st-tab\s*\{[^}]*flex\s*:\s*1")
        self.assertRegex(mobile, r"\.st-tab\s*\{[^}]*font-size\s*:\s*12px")
        self.assertRegex(mobile, r"\.st-header\s+#theme-btn\s*\{[^}]*width\s*:\s*44px")

    def test_request_cells_expose_all_nine_column_labels(self):
        labels = (
            "Time", "Status", "Prompt", "Reused", "Output", "Prefill t/s",
            "Decode t/s", "VRAM hit rate", "Duration",
        )
        for label in labels:
            with self.subTest(label=label):
                self.assertTrue(f'data-label="{label}"' in APP_JS, f"missing data label: {label}")

    def test_request_table_keeps_semantic_headers_and_hides_them_visually(self):
        self.assertIn("<thead>", INDEX)
        self.assertEqual(INDEX.count('scope="col"'), 9, "all nine table headers need scope=col")
        pattern = r"#req-wrap\s+thead\s*\{[^}]*clip-path\s*:\s*inset\(50%\)"
        self.assertIsNotNone(re.search(pattern, APP_CSS), "table headers must be visually hidden, not removed")

    def test_mobile_requests_render_as_labeled_cards_without_table_scrolling(self):
        self.assertIsNotNone(re.search(r"@media\s*\(max-width:\s*640px\)", APP_CSS), "mobile breakpoint missing")
        pattern = r"#req-wrap\s+\.st-table\s+tbody\s+tr\s*\{[^}]*display\s*:\s*grid"
        self.assertIsNotNone(re.search(pattern, APP_CSS), "request rows must become cards")
        self.assertIn("content: attr(data-label)", APP_CSS, "visible field labels missing")
        pattern = r"#req-wrap\s*\{[^}]*overflow\s*:\s*visible"
        self.assertIsNotNone(re.search(pattern, APP_CSS), "request table must not scroll horizontally")

    def test_narrow_header_and_metrics_are_compact_at_320px(self):
        self.assertIsNotNone(re.search(r"@media\s*\(max-width:\s*360px\)", APP_CSS), "320px breakpoint missing")
        pattern = r"\.st-header\s*\{[^}]*min-width\s*:\s*0"
        self.assertIsNotNone(re.search(pattern, APP_CSS), "header items must be allowed to shrink")
        pattern = r"#theme-btn\s*\{[^}]*flex\s*:\s*none"
        self.assertIsNotNone(re.search(pattern, APP_CSS), "theme control must keep a fixed tap target")
        narrow = APP_CSS.split("@media (max-width: 360px)", 1)[1]
        self.assertRegex(narrow, r"\.st-tab\s*\{[^}]*height\s*:\s*44px")
        self.assertRegex(narrow, r"\.st-tab\s*\{[^}]*font-size\s*:\s*10px")
        self.assertRegex(narrow, r"\.st-tab\s*\{[^}]*padding-inline\s*:\s*1px")
        self.assertRegex(narrow, r"#theme-btn\s*\{[^}]*height\s*:\s*44px")
        self.assertRegex(narrow, r"\.metric-card\s*\{[^}]*padding")
        self.assertRegex(narrow, r"\.metrics\s*\{[^}]*gap")


if __name__ == "__main__":
    unittest.main()
