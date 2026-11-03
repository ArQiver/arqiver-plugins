#!/usr/bin/env python3
"""Offline package contract and installer checks (no network or credentials)."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('package', ROOT / 'scripts/package.py')
pkg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pkg)

class Packages(unittest.TestCase):
    def test_manifests(self):
        p = ROOT / 'plugins/arqiver'
        manifests = [json.loads((p / f).read_text()) for f in
                     ['plugin.json', '.claude-plugin/plugin.json', '.codex-plugin/plugin.json']]
        self.assertEqual({x['name'] for x in manifests}, {'arqiver'})
        self.assertEqual(len({x['version'] for x in manifests}), 1)
        for market in ['.claude-plugin/marketplace.json', '.agents/plugins/marketplace.json']:
            m = json.loads((ROOT / market).read_text())
            source = m['plugins'][0]['source']
            path = source['path'] if isinstance(source, dict) else source
            self.assertTrue((ROOT / path / 'plugin.json').is_file())
        for skill in (p / 'skills').glob('*/SKILL.md'):
            text = skill.read_text()
            self.assertTrue(text.startswith('---\nname: '))
            self.assertIn('\ndescription: ', text)
            self.assertIn('\n---\n', text)
        self.assertEqual(len(list((p / 'skills').glob('*/SKILL.md'))), 3)

    def test_generated_packages(self):
        old = pkg.ROOT
        with tempfile.TemporaryDirectory() as tmp:
            import shutil
            root = Path(tmp)
            for name in ['plugins', '.agents', '.claude-plugin']:
                shutil.copytree(ROOT / name, root / name)
            shutil.copy2(ROOT / 'LICENSE', root / 'LICENSE')
            pkg.ROOT = root
            try:
                out = pkg.package('https://demo.arqiver.com/mcp', 'demo')
                for name in ['mcp.json', '.mcp.json']:
                    data = json.loads((out / 'plugins/arqiver' / name).read_text())
                    self.assertEqual(data['mcpServers']['arqiver']['url'], 'https://demo.arqiver.com/mcp')
                for name in ['.agents/plugins/marketplace.json', '.claude-plugin/marketplace.json']:
                    self.assertEqual(json.loads((out / name).read_text())['name'], 'arqiver-demo')
                self.assertTrue((out / 'plugins/arqiver/LICENSE').exists())
                with self.assertRaises(ValueError):
                    pkg.package('https://demo.arqiver.com/mcp', 'demo')
                with self.assertRaises(ValueError):
                    pkg.package('https://demo.arqiver.com/mcp', '../escape')
            finally:
                pkg.ROOT = old

    def test_url_validation(self):
        for value in ['http://demo.arqiver.com/mcp', 'https://tenant.example/mcp',
                      'https://user:secret@demo.arqiver.com/mcp',
                      'https://demo.arqiver.com/mcp?token=secret',
                      'https://demo.arqiver.com/mcp#token', 'https://demo.arqiver.com/']:
            with self.subTest(value=value), self.assertRaises(Exception):
                pkg.validate_url(value)
        self.assertEqual(pkg.validate_url('https://demo.arqiver.com/mcp/'),
                         'https://demo.arqiver.com/mcp')

if __name__ == '__main__':
    unittest.main()
