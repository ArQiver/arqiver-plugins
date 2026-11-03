#!/usr/bin/env python3
"""Read-only MCP/OAuth discovery check; never signs in or creates a grant."""
import argparse
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, HTTPRedirectHandler, build_opener
from package import validate_url

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('Unexpected redirect; use the canonical tenant endpoint')

def fetch(url):
    if urlsplit(url).scheme != 'https':
        raise ValueError('Discovery requires HTTPS')
    with build_opener(NoRedirect).open(Request(url, headers={'Accept': 'application/json'}), timeout=15) as response:
        body = response.read(1048577)
        if len(body) > 1048576:
            raise ValueError('Discovery document exceeds 1 MiB')
        return json.loads(body)

def probe(url):
    origin = url.rsplit('/mcp', 1)[0]
    resource = fetch(origin + '/.well-known/oauth-protected-resource')
    if resource.get('resource', '').rstrip('/') != url:
        raise ValueError('OAuth resource does not match the selected MCP URL')
    issuers = resource.get('authorization_servers', [])
    if not issuers:
        raise ValueError('No OAuth authorization server advertised')
    issuer = issuers[0].rstrip('/')
    u = urlsplit(issuer)
    # ArQiver advertises an origin issuer; refuse unsupported path issuers explicitly.
    if u.path or u.query or u.fragment or u.username or u.password:
        raise ValueError('Expected an origin-only OAuth issuer')
    auth = fetch(issuer + '/.well-known/oauth-authorization-server')
    for key in ['authorization_endpoint', 'token_endpoint', 'registration_endpoint']:
        endpoint = urlsplit(auth.get(key, ''))
        if endpoint.scheme != 'https' or not endpoint.hostname:
            raise ValueError('Missing HTTPS ' + key)
    if 'S256' not in auth.get('code_challenge_methods_supported', []):
        raise ValueError('OAuth does not advertise PKCE S256')
    print('MCP resource and OAuth discovery ready (including registration and PKCE).')
    print('Browser sign-in, permissions and document actions still require a host connection test.')

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--url', type=validate_url, required=True)
    args = p.parse_args()
    try:
        probe(args.url)
    except (HTTPError, URLError, ValueError, KeyError) as error:
        p.exit(1, 'Discovery check failed: ' + str(error) + '\n')
