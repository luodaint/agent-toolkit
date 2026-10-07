#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: update-toolkit.sh [--check] [--path PATH] [--branch BRANCH]

Run from a consuming project's Git working tree. Fetch the toolkit submodule's
origin/main and select its latest commit without staging or committing the pin.

  --check          Fetch and preview changes without switching commits.
  --path PATH      Submodule path relative to the project root (.agents/toolkit).
  --branch BRANCH  Remote branch to fetch (main).
  -h, --help       Show this help.

Requires Bash and Git. Initialize the submodule first. Refuses local changes,
staged pin changes and updates that would leave commits outside the new history.
EOF
}

fail() {
  printf 'Update stopped: %s\n' "$*" >&2
  exit 1
}

# Keep execution in a function: checking out an update may replace this script.
main() {
  local preview=false module_path=.agents/toolkit branch=main
  local parent module registered_parent entry before after
  while (( $# )); do
    case "$1" in
      --check) preview=true; shift ;;
      --path|--branch)
        (( $# >= 2 )) || fail "Missing value for $1."
        [[ -n "$2" ]] || fail "Empty value for $1."
        if [[ "$1" == --path ]]; then module_path=$2; else branch=$2; fi
        shift 2 ;;
      -h|--help) usage; return ;;
      *) fail "Unknown argument: $1. Use --help." ;;
    esac
  done

  command -v git >/dev/null || fail 'Git is required.'
  git check-ref-format "refs/heads/$branch" >/dev/null || fail 'Invalid branch name.'
  case "$module_path" in
    /*|.|..|../*|*/../*|*/..|./*|*/./*|*/.|*/|*//* )
      fail 'Use a normalized relative submodule path.' ;;
  esac
  parent=$(git rev-parse --show-toplevel) || fail 'Run inside the consuming project.'
  parent=$(cd "$parent" && pwd -P)
  entry=$(git -C "$parent" --literal-pathspecs -c core.quotePath=false ls-files --stage -- "$module_path")
  [[ "$entry" == "160000 "* ]] || fail 'Path is not a registered submodule.'
  [[ -d "$parent/$module_path" ]] || fail 'Initialize the submodule first.'
  module=$(cd "$parent/$module_path" && pwd -P)
  registered_parent=$(git -C "$module" rev-parse --show-superproject-working-tree)
  [[ -n "$registered_parent" ]] || fail 'Initialize the submodule first.'
  registered_parent=$(cd "$registered_parent" && pwd -P)
  [[ "$registered_parent" == "$parent" ]] || fail 'Submodule belongs to another project.'
  git -C "$parent" --literal-pathspecs diff --cached --quiet -- "$module_path" ||
    fail 'The submodule pin has staged changes; preserve that update first.'
  [[ -z "$(git -C "$module" status --porcelain --untracked-files=all)" ]] ||
    fail 'The submodule has local changes; commit or preserve them first.'

  before=$(git -C "$module" rev-parse --verify HEAD)
  git -C "$module" fetch --no-tags origin "refs/heads/$branch"
  after=$(git -C "$module" rev-parse --verify 'FETCH_HEAD^{commit}')
  git -C "$module" merge-base --is-ancestor "$before" "$after" ||
    fail 'Current commits are outside the fetched history. Preserve local commits or inspect divergence/shallow history manually.'

  printf 'Current: %s\nLatest origin/%s: %s\n' "$before" "$branch" "$after"
  if [[ "$before" == "$after" ]]; then
    printf 'Toolkit is already up to date.\n'
    return
  fi
  git -C "$module" log --oneline "$before..$after"
  git -C "$module" diff --stat "$before" "$after"
  if [[ "$preview" == true ]]; then
    printf 'Preview only: the checkout and parent pin are unchanged.\n'
    return
  fi

  git -C "$module" checkout --no-overwrite-ignore --detach "$after"
  printf '\nSelected the latest toolkit commit. The parent index is unchanged.\n'
  printf 'Review the submodule diff and updated instructions, validate, then commit\n'
  printf 'the new pin through the consuming project\047s normal review process.\n'
  printf 'Previous toolkit commit (for rollback): %s\n' "$before"
}

main "$@"
