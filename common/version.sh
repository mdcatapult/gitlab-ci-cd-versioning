#! /bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# shellcheck source=.
. "$DIR/utils.sh"

git commit --allow-empty -am "Setting version to ${RELEASE_TAG}"
reportError $?

git push origin "$CI_COMMIT_BRANCH"
reportError $?

git tag -a "${RELEASE_TAG}" -m "Setting version to ${RELEASE_TAG}"
reportError $?

git push origin --tags
reportError $?
