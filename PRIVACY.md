# Plugin data handling

The package runs no hosted service and collects no telemetry. Its packaging
script writes the selected MCP endpoint into a local package; it never requests
or stores access tokens. OAuth credentials are managed by Claude or Codex.

The assistant connects directly to the configured ArQiver tenant. Authorized
content it reads is transmitted to and processed by the assistant provider.
ArQiver access rules and the OAuth consent determine the available data and
operations. The tenant operator's and assistant provider's privacy terms apply;
this document describes the package, not those services' contractual policies.

For questions about a tenant's retention or processing terms, contact that tenant's
operator. Do not publish generated tenant packages without checking their endpoint
and the operator's distribution requirements.
