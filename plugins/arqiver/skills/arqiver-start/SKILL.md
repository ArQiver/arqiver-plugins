---
name: arqiver-start
description: Connect to ArQiver and discover the authorized document streams, sets and available MCP workflows.
---

Use the installed ArQiver MCP server. Call `guide` without a topic first, then
`find_actions` for the requested task. Read the returned schemas before calling
an action. Use `read_action` for read actions and `call_action` for changes.
The server catalogue is authoritative: capabilities vary by deployed version.

Use the connected tenant and the user's existing permissions. If authentication
is needed, use the host's MCP OAuth sign-in. Never ask for passwords or tokens in
chat. If disconnected, point to the plugin README setup and the host's MCP status.
Do not silently switch tenants or environments.

Read permits authorized document content and screen selections; propose permits
sets and mapper proposals; design permits shared draft stream/card composition.
Request only permissions needed by the user's task. This plugin defaults to read
and propose, not design. ArQiver's consent screen controls the actual grant.

Explain that document content read through MCP is processed by the assistant's
provider when relevant to the user's connection decision. Use server links to
return the user to the matching ArQiver context.
