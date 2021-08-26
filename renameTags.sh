#!/bin/bash

set -e
git tag -l | while read t; do if [[ $t == t* ]]; then echo "$t already has the demanded format"; else n="t$t"; git tag $n refs/tags/$t; git tag -d $t; fi; done
