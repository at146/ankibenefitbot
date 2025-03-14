#!/bin/bash

ver=$(git describe --abbrev=0 --tags)  # v1.2.0
semver=(${ver/v})  # semver - 1.2.0
arrIN=(${semver//./ })  # [1, 2, 0]
next_minor=$((arrIN[1] + 1))
next_ver=${arrIN[0]}.$next_minor.${arrIN[2]}

git tag "v$next_ver"

git push --tags
