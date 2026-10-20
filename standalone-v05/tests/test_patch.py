"""Offline source and workflow smoke tests. Not a substitute for a macOS build."""
from __future__ import annotations
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from patch_quick_panel import patch_source, SIGNATURE, QUICK_PANEL_SWIFT


class QuickPanelTests(unittest.TestCase):
    def source_root(self, tmp: Path) -> Path:
        file = tmp / "TLocation" / "Views" / "RootView.swift"
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text('''import SwiftUI
import UIKit
struct RootView: View {
    @State private var isShowingSettings = false
    var body: some View {
        NavigationStack {
            ZStack { Text("Placeholder") }
            .animation(.easeInOut(duration: 0.2), value: isReady)
        }
        .sheet(isPresented: $isShowingSettings) {
            SettingsView()
        }
    }
}
''', encoding="utf-8")
        return tmp

    def test_appends_panel_and_connects_existing_commands(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            root = self.source_root(Path(d))
            updated = patch_source(root).read_text(encoding="utf-8")
            self.assertIn(SIGNATURE, updated)
            self.assertIn('PersonalGPS · Hold for GPS', updated)
            self.assertIn('LocationSimulationRequest.postSimulate(latitude: lat, longitude: lon)', updated)
            self.assertIn('LocationSimulationRequest.postClear()', updated)
            self.assertIn('guard let lat = Double(', updated)
            self.assertIn('MapReader { reader in', updated)
            self.assertIn('import MapKit', updated)

    def test_prevents_duplicate_patch(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            root = self.source_root(Path(d))
            patch_source(root)
            with self.assertRaisesRegex(ValueError, 'already installed'):
                patch_source(root)

    def test_rejects_changed_upstream(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            root = self.source_root(Path(d))
            file = root / 'TLocation' / 'Views' / 'RootView.swift'
            file.write_text(file.read_text().replace('isShowingSettings', 'settingsBool'))
            with self.assertRaisesRegex(ValueError, 'Pinned upstream UI mismatch'):
                patch_source(root)

    def test_quick_panel_does_not_replace_engine(self) -> None:
        self.assertNotIn('simulate_location(', QUICK_PANEL_SWIFT)
        self.assertNotIn('clear_simulated_location(', QUICK_PANEL_SWIFT)
        self.assertNotIn('isSimulatedBySoftware', QUICK_PANEL_SWIFT)
        self.assertIn('Return to Real Location', QUICK_PANEL_SWIFT)


if __name__ == '__main__':
    unittest.main()
