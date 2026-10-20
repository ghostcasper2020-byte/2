import tempfile
import json
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rebrand import BUNDLE_ID, DISPLAY_NAME, update_project

class RebrandTests(unittest.TestCase):
    def test_expected_source_is_modified(self):
        with tempfile.TemporaryDirectory() as tmp:
            x = Path(tmp) / 'TLocation.xcodeproj'
            x.mkdir()
            pbx = x / 'project.pbxproj'
            catalog = Path(tmp) / 'TLocation' / 'InfoPlist.xcstrings'
            catalog.parent.mkdir()
            catalog.write_text(json.dumps({'strings': {'CFBundleDisplayName': {'localizations': {'en': {'stringUnit': {'value': 'TLocation'}}}}, 'CFBundleName': {'localizations': {'en': {'stringUnit': {'value': 'TLocation'}}}}}}))
            pbx.write_text(('INFOPLIST_KEY_CFBundleDisplayName = TLocation;\n' +
                            'PRODUCT_BUNDLE_IDENTIFIER = vn.truongkma.tlocation;\n') * 2)
            update_project(Path(tmp))
            result = pbx.read_text()
            self.assertEqual(result.count('INFOPLIST_KEY_CFBundleDisplayName = '+DISPLAY_NAME+';'), 2)
            self.assertEqual(result.count('PRODUCT_BUNDLE_IDENTIFIER = '+BUNDLE_ID+';'), 2)
            self.assertNotIn('PRODUCT_BUNDLE_IDENTIFIER = vn.truongkma.tlocation;', result)
            self.assertEqual(json.loads(catalog.read_text())['strings']['CFBundleDisplayName']['localizations']['en']['stringUnit']['value'], DISPLAY_NAME)

    def test_unexpected_upstream_source_refuses_modify(self):
        with tempfile.TemporaryDirectory() as tmp:
            x = Path(tmp) / 'TLocation.xcodeproj'
            x.mkdir()
            pbx = x / 'project.pbxproj'
            original = 'PRODUCT_BUNDLE_IDENTIFIER = something.else;'
            pbx.write_text(original)
            with self.assertRaises(ValueError):
                update_project(Path(tmp))
            self.assertEqual(pbx.read_text(), original)

if __name__ == '__main__':
    unittest.main()
