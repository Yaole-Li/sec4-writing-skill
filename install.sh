#!/usr/bin/env bash
# Install the security-conf-writing skill for Claude Code and/or Codex (DeepSeek Harness uses ~/.agents).
# Usage: ./install.sh [claude|codex|all] [--project]
set -euo pipefail
target="${1:-all}"; scope="${2:-}"
src="$(cd "$(dirname "$0")" && pwd)/skills/security-conf-writing"
[ -f "$src/SKILL.md" ] || { echo "SKILL.md not found in $src" >&2; exit 1; }
install_to() {
  local dir="$1"
  mkdir -p "$dir"
  rm -rf "$dir/security-conf-writing"
  cp -R "$src" "$dir/security-conf-writing"
  echo "Installed to $dir/security-conf-writing"
}
if [ "$scope" = "--project" ]; then claude_dir=".claude/skills"; codex_dir=".agents/skills"
else claude_dir="$HOME/.claude/skills"; codex_dir="$HOME/.agents/skills"; fi
case "$target" in
  claude) install_to "$claude_dir" ;;
  codex)  install_to "$codex_dir" ;;
  all)    install_to "$claude_dir"; install_to "$codex_dir" ;;
  *) echo "Usage: $0 [claude|codex|all] [--project]" >&2; exit 1 ;;
esac
echo "Restart your agent if the skill does not show up."
