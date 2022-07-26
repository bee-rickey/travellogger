#!/usr/bin/env bash

set -eu
env
repo_uri="https://x-access-token:${MY_TOKEN}@github.com/travellogger.git"

echo "$repo_url"
remote_name="origin"
main_branch="master"
gh_pages_branch="gh-pages"


git config user.name "$GITHUB_ACTOR"
git config user.email "${GITHUB_ACTOR}@bots.github.com"

git checkout "$main_branch"

python3 start.py

git add .
set +e  # Grep succeeds with nonzero exit codes to show results.

if git status | grep 'new file\|modified'
then
    set -e
    git commit -am "data updated on - $(date)"
    git remote set-url "$remote_name" "$repo_uri" # includes access token
    git push --force-with-lease "$remote_name" "$main_branch"
else
    set -e
    echo "No changes since last run"
fi

echo "finish"
