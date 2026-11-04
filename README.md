# ArQiver plugins for Claude and Codex

Connect an assistant to your ArQiver tenant through its remote MCP server.
Inspired by [ClosetMatchR's Claude marketplace](https://github.com/ClosetMatchR/closetmatchr-plugins).
This is an ArQiver-maintained package, not an endorsement by Anthropic or OpenAI.

- **Start:** discover accessible streams and current server capabilities.
- **Documents:** investigate extracted text and metadata with verifiable evidence.
- **Patterns:** propose category rules, preview joining/leaving documents, then apply a chosen preview.

Shared skills; Claude manifest, portable Agent Plugins manifest, Codex compatibility
manifest and marketplace catalogs. No local MCP server, runtime dependency or
embedded credentials. Python 3 is used only to build the configured package.

## Install the Waterdam demo

The repository plugin connects directly to the current **Waterdam demo**, through
its public HTTPS ngrok endpoint. No packaging step, zip or URL entry is needed.
This is demo data, not a production tenant. The tunnel and Mac runtime must stay
running. If the tunnel URL changes, the repository connector must be updated and
your installed plugin refreshed.

### Claude

Add `ArQiver/arqiver-plugins` as a plugin marketplace, install **arqiver**, then
click **Connect** and complete the ArQiver sign-in. If already installed, refresh
the marketplace and update the plugin to **0.1.3** (reinstall if the host keeps
showing the old connector).

```sh
claude plugin marketplace add ArQiver/arqiver-plugins
claude plugin install arqiver@arqiver-local
```

### Codex

```sh
codex plugin marketplace add ArQiver/arqiver-plugins
codex plugin add arqiver@arqiver-local
```

Restart the session and follow OAuth sign-in. No token belongs in the plugin.

## Optional: another environment

For operators who need a different tenant, generate a separate local package:

```sh
git clone https://github.com/ArQiver/arqiver-plugins.git
cd arqiver-plugins
python3 scripts/probe.py --url https://YOUR-TENANT.arqiver.com/mcp
python3 scripts/package.py --name my-tenant --url https://YOUR-TENANT.arqiver.com/mcp
```

This creates `dist/my-tenant`, a local marketplace named `arqiver-my-tenant`.
It contains the chosen endpoint, never credentials. The following local-marketplace
instructions apply only to this optional configuration.

## Claude Code

Use a current Claude Code with plugin and remote HTTP MCP support:

```sh
claude plugin marketplace add "$PWD/dist/my-tenant"
claude plugin install arqiver@arqiver-my-tenant
```

Start a new session, open `/mcp`, select ArQiver and complete browser sign-in and
consent. Try `/arqiver:arqiver-start`. Claude Desktop marketplace support can vary;
where unavailable, add a custom remote connector with the same `/mcp` URL in its
connector settings. That fallback connects tools but does not install these skills.

## Codex

Use a current Codex with plugin marketplace support:

```sh
codex plugin marketplace add "$PWD/dist/my-tenant"
codex plugin add arqiver@arqiver-my-tenant
```

Start a new session and follow the MCP OAuth connection prompt. If authentication
is not offered, inspect `/mcp` and the host's connection settings. Ask to use
`arqiver-start`. The package declares OAuth dynamic client registration; no client
secret is required. The portable manifest is preferred on newer hosts; the
`.codex-plugin` and `.mcp.json` files support compatibility hosts.

For a tools-only fallback, `codex mcp add arqiver --url https://YOUR-TENANT.arqiver.com/mcp`
and `codex mcp login arqiver` register it directly. This does not install skills;
remove that direct registration before enabling the plugin to avoid duplicate tools.

## Verify the connection

Ask: “Use ArQiver's guide and show me the streams I can access.” The assistant
should call `guide`, discover the relevant actions with `find_actions`, then use
`read_action`. It should never ask you to paste a password or token.

For categories: “Explore invoice patterns in this stream. Preview a candidate
and show joining and leaving examples before applying anything.” This should use
`get_set_rule_context`, `get_document_page`, `preview_document_selection`
and paginated `get_set_rule_preview`. The server derives layout rules and offers
the mapper's supported value conversions. Missing optional field values stay in
the set; only explicitly required field recognition can exclude them. Only the chosen change uses
`apply_set_rule_preview`. A preview does not appear in the browser's local concept;
an applied set appears in the normal ArQiver workspace.

## Permissions and data

OAuth uses your existing ArQiver account and stream permissions. Default scopes:
`read` and `propose`. The consent screen controls the actual grant; read-only
connections cannot apply sets. `design` is optional and is not requested here;
it allows shared draft stream/card design. Routing and publishing stay in ArQiver's
human workflow. Documents read through MCP are processed by the assistant provider.
Disconnect/revoke access through ArQiver's AI assistants page and the host's settings.

## Troubleshooting

- **404 on MCP/discovery:** deploy MCP to that tenant first; a plugin cannot add server capabilities.
- **401:** normal before OAuth; complete sign-in. Do not place bearer tokens in manifests.
- **Missing patterns domain:** the server needs the automatic-set MCP actions deployed.
- **403/permission error:** inspect stream access and OAuth scopes; reconnect if consent needs changing.
- **Expired/stale preview:** compute and inspect a fresh preview before applying.
- **Updated package:** regenerate to a new output name or explicitly remove the previous generated directory,
  refresh the local marketplace in your host and restart the session. Never delete source files to update.

This repo is an installable local/repo marketplace, **not a public-directory listing**.
ChatGPT's public directory requires separate MCP registration, testing and review.
No host settings or live data are changed by the packaging script.

## Development

```sh
python3 scripts/check.py
claude plugin validate --strict plugins/arqiver
claude plugin validate --strict .claude-plugin/marketplace.json
```

CI checks the shared package and tenant generation offline. Actual OAuth and real
preview/apply journeys must also be checked against the target deployed tenant.
Official formats: [OpenAI plugins](https://developers.openai.com/plugins/build/plugins),
[Claude plugins](https://code.claude.com/docs/en/plugins-reference).

[Package privacy and data handling](PRIVACY.md).
