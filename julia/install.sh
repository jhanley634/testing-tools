#! /usr/bin/env bash

# Ensures that needed libary packages are available.
#
# Tested on ubuntu trusty tahr.

set -e -x

julia <<'EOF'
Pkg.update()
Pkg.add("PyCall")
EOF

sudo -H pip install pydot
python -c 'import pydot'
