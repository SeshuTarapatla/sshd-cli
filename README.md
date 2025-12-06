# sshd-cli

A Textual-based TUI tool that bootstraps personal SSHD instances on remote VMs over existing GSSAPI/Kerberos SSH connections.

## Why?

When your organization's SSH server disables TCP port forwarding, VS Code Remote Development doesn't work. **sshd-cli** solves this by:

- Connecting via your existing GSSAPI auth (no passwords)
- Setting up a personal `~/.ssh` environment (config, host keys, authorized_keys)
- Launching SSHD on an unprivileged port with full port-forwarding support
- One-click VS Code Remote session launch
- Clean shutdown — kills remote SSHD and local VS Code on exit

## Features

- 🖥️ **Host Management** — Add, edit, remove remote VMs
- 🔐 **Automatic Setup** — Generates and syncs SSH keys/configs
- 🚀 **One-Click VS Code** — Launch remote dev sessions instantly
- 🧹 **Graceful Cleanup** — No orphaned processes left behind