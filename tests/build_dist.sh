#!/usr/bin/env bash
# Builds the two upload-ready skill zips in dist/ for the Claude app (Settings > Capabilities > Skills > Upload skill).
# find-my-job.zip bundles scripts/ and data/ inside the skill folder so it works as a standalone skill.
# Run from the repo root after any change to a skill, the scripts or the company pool: bash tests/build_dist.sh
set -eu
P=plugins/gtm-job-search
T=$(mktemp -d)
mkdir -p dist "$T/find-my-job" "$T/gtm-resume-tailor"
cp -R $P/skills/find-my-job/. "$T/find-my-job/"
cp -R $P/scripts "$T/find-my-job/scripts"
cp -R $P/data "$T/find-my-job/data"
cp -R $P/skills/gtm-resume-tailor/. "$T/gtm-resume-tailor/"
find "$T" -name __pycache__ -prune -exec rm -rf {} +
rm -f dist/find-my-job.zip dist/gtm-resume-tailor.zip
(cd "$T" && zip -qr "$OLDPWD/dist/find-my-job.zip" find-my-job && zip -qr "$OLDPWD/dist/gtm-resume-tailor.zip" gtm-resume-tailor)
echo "built dist/find-my-job.zip and dist/gtm-resume-tailor.zip"
