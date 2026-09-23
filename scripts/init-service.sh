#!/usr/bin/env bash
set -euo pipefail

# Copy the Python service scaffold and Cursor *service* rules into a new repo.
# Does not copy pipeline skills/agents — those stay in the orchestrator workspace.

if [[ $# -ne 1 ]]; then
  echo "Usage: scripts/init-service.sh /path/to/new-service" >&2
  exit 1
fi

destination="$1"
script_dir="$(cd "$(dirname "$0")" && pwd)"
config_root="$(cd "${script_dir}/.." && pwd)"
template_root="${config_root}/template"

if [[ ! -d "${template_root}" ]]; then
  echo "Template not found at ${template_root}" >&2
  exit 1
fi

mkdir -p "${destination}"
cp -R "${template_root}/." "${destination}/"
mkdir -p "${destination}/.cursor"
cp -R "${config_root}/.cursor/rules" "${destination}/.cursor/"
cp -R "${config_root}/.cursor/roles" "${destination}/.cursor/"

echo "Service scaffold copied to ${destination}"
echo "Included: template code, .github CI, .cursor/rules, .cursor/roles"
echo "Not included: pipeline skill or agents (run /implement-task from the orchestrator workspace)"
