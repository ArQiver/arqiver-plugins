#!/usr/bin/env python3
"""Generate a tenant-specific local marketplace; never modify installed hosts."""
import argparse
import json
from pathlib import Path
import shutil
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]

def validate_url(value):
    u = urlsplit(value)
    if (u.scheme != "https" or not u.hostname or u.username or u.password
            or u.query or u.fragment or u.path.rstrip("/") != "/mcp"
            or u.hostname.endswith(".example")):
        raise argparse.ArgumentTypeError("Use your tenant's HTTPS /mcp URL without credentials, query or fragment")
    return value.rstrip("/")

def package(url, name):
    url = validate_url(url)
    if not name or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in name):
        raise ValueError("name must contain lowercase letters, digits or hyphens")
    out = ROOT / "dist" / name
    if out.exists():
        raise ValueError(f"Output already exists: {out}; remove it explicitly to regenerate")
    out.mkdir(parents=True)
    for path in ("plugins", ".claude-plugin", ".agents"):
        shutil.copytree(ROOT / path, out / path)
    shutil.copy2(ROOT / "LICENSE", out / "plugins/arqiver/LICENSE")
    for path, template in (("plugins/arqiver/mcp.json", "portable-mcp.json"),
                           ("plugins/arqiver/.mcp.json", "claude-mcp.json")):
        p = out / path
        data = json.loads((ROOT / "templates" / template).read_text())
        data["mcpServers"]["arqiver"]["url"] = url
        p.write_text(json.dumps(data, indent=2) + "\n")
    for path in (".claude-plugin/marketplace.json", ".agents/plugins/marketplace.json"):
        p = out / path
        data = json.loads(p.read_text())
        data["name"] = "arqiver-" + name
        p.write_text(json.dumps(data, indent=2) + "\n")
    return out

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--url", type=validate_url, required=True)
    p.add_argument("--name", default="local", help="local marketplace suffix, e.g. waterdam")
    a = p.parse_args()
    try:
        print(package(a.url, a.name))
    except ValueError as e:
        p.error(str(e))
