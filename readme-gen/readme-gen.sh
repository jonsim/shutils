#!/bin/sh
# (c) Copyright 2017 Jonathan Simmonds
# Simple, not hugely robust script, to automatically generate the documentation
# for each shutil from its -h option and example scripts.
set -e

if [ $# -ne 0 ]; then
    echo "usage: readme-gen.sh [-h]"
    echo ""
    echo "Simple, not hugely robust, script to automatically generate the"
    echo "documentation for all shutils. This is done by: for all"
    echo "<shutil>.examples.sh files alongside this script, running:"
    echo "  <shutil> -h"
    echo "to retrieve its usage information and running:"
    echo "  sh -v <shutil>.examples.sh"
    echo "to generate the example information."
    echo ""
    echo "optional arguments:"
    echo "  -h, --help         Print this message and exit"
    exit
fi

SCRIPT_DIR=$(readlink -f "$0" | xargs dirname)
SHUTIL_DIR="${SCRIPT_DIR}/.."
RM_HEADER="${SCRIPT_DIR}/readme-header.md"
RM_USAGE="${SCRIPT_DIR}/readme-usage.md"
RM_FOOTER="${SCRIPT_DIR}/readme-footer.md"
RM_FINAL="${SHUTIL_DIR}/README.md"

# Generate usage readme
echo "## Documentation"  > ${RM_USAGE}
echo '---'              >> ${RM_USAGE}

# List all example scripts
EXAMPLE_SCRIPTS=$(find ${SCRIPT_DIR} -maxdepth 1 -type f -name '*.examples.sh' -printf '%f\n' | sort)
for EXAMPLE in ${EXAMPLE_SCRIPTS}; do
    # Calculate the shutil from the example file.
    SHUTIL=$(echo ${EXAMPLE} | sed -e 's/\.examples\.sh//g')
    # Write the .md
    # Write title
    echo "### ${SHUTIL}"                                        >> ${RM_USAGE}
    # Write type
    echo "#### Type"                                            >> ${RM_USAGE}
    file --b ${SHUTIL_DIR}/${SHUTIL} | sed -e 's/,.*$//'        >> ${RM_USAGE}
    echo ""                                                     >> ${RM_USAGE}
    # Write usage
    echo "#### Usage"                                           >> ${RM_USAGE}
    echo '```'                                                  >> ${RM_USAGE}
    set +e
    PATH=${SHUTIL_DIR}:${PATH} ${SHUTIL} -h                     >> ${RM_USAGE}
    set -e
    echo '```'                                                  >> ${RM_USAGE}
    echo ""                                                     >> ${RM_USAGE}
    # Write examples
    echo "#### Examples"                                        >> ${RM_USAGE}
    echo '```sh'                                                >> ${RM_USAGE}
    PATH=${SHUTIL_DIR}:${PATH} sh -v ${SCRIPT_DIR}/${EXAMPLE}   >> ${RM_USAGE} 2>&1
    echo '```'                                                  >> ${RM_USAGE}
    echo '---'                                                  >> ${RM_USAGE}
    echo ""                                                     >> ${RM_USAGE}
done

# Merge header and usage into destination readme.
cat ${RM_HEADER} ${RM_USAGE} ${RM_FOOTER} > ${RM_FINAL}