#!/bin/sh
# (c) Copyright 2017 Jonathan Simmonds
# Simple, not hugely robust script, to automatically generate the documentation
# for each shutil from its -h option and example scripts.
set -e

SCRIPT_DIR=$(readlink -f "$0" | xargs dirname)
SHUTIL_DIR="${SCRIPT_DIR}/.."
RM_HEADER="${SCRIPT_DIR}/readme-header.md"
RM_TOC="${SCRIPT_DIR}/readme-toc.md"
RM_USAGE="${SCRIPT_DIR}/readme-usage.md"
RM_FOOTER="${SCRIPT_DIR}/readme-footer.md"
RM_FINAL="${SHUTIL_DIR}/README.md"

# Output usage information and exit.
usage()
{
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
    echo "  -h, --help      Print this message and exit."
    exit 1
}

# Generate a TOC entry line.
# Args:
#   $1  the name of the TOC entry to generate.
#   $2  the level of the TOC entry to generate.
gen_toc_entry()
{
    ENTRY_NAME="$1"
    LINK_NAME=$(echo ${ENTRY_NAME} | tr '[:upper:]' '[:lower:]')
    printf "%${2}s" >> ${RM_TOC}
    echo "- [${ENTRY_NAME}](#${LINK_NAME})" >> ${RM_TOC}
}

if [ $# -ne 0 ]; then
    usage
fi

# Generate table of contents
echo "# Table of Contents"   > ${RM_TOC}
gen_toc_entry "shutils" "1"
gen_toc_entry "Installation" "1"
gen_toc_entry "License" "1"
gen_toc_entry "Documentation" "1"

# Generate usage readme
echo "# Documentation"  > ${RM_USAGE}

# List all example scripts
EXAMPLE_SCRIPTS=$(find ${SCRIPT_DIR} -maxdepth 1 -type f -name '*.examples.sh' -printf '%f\n' | sort)
for EXAMPLE in ${EXAMPLE_SCRIPTS}; do
    # Calculate the shutil from the example file.
    SHUTIL=$(echo ${EXAMPLE} | sed -e 's/\.examples\.sh//g')
    # Write the .md
    # Write title
    echo "## ${SHUTIL}"                                         >> ${RM_USAGE}
    gen_toc_entry "${SHUTIL}" "2"
    # Write type
    echo "#### Type"                                            >> ${RM_USAGE}
    gen_toc_entry "Type" "4"
    file --b ${SHUTIL_DIR}/${SHUTIL} | sed -e 's/,.*$//'        >> ${RM_USAGE}
    echo ""                                                     >> ${RM_USAGE}
    # Write usage
    echo "#### Usage"                                           >> ${RM_USAGE}
    gen_toc_entry "Usage" "4"
    echo '```'                                                  >> ${RM_USAGE}
    set +e
    PATH=${SHUTIL_DIR}:${PATH} ${SHUTIL} -h                     >> ${RM_USAGE}
    set -e
    echo '```'                                                  >> ${RM_USAGE}
    echo ""                                                     >> ${RM_USAGE}
    # Write examples
    echo "#### Examples"                                        >> ${RM_USAGE}
    gen_toc_entry "Examples" "4"
    echo '```sh'                                                >> ${RM_USAGE}
    PATH=${SHUTIL_DIR}:${PATH} sh ${SCRIPT_DIR}/${EXAMPLE} 2>&1 \
                | sed -e 's/^set +v$//g'                        >> ${RM_USAGE}
    echo '```'                                                  >> ${RM_USAGE}
    echo ""                                                     >> ${RM_USAGE}
done

echo "" >> ${RM_TOC}

# Merge header and usage into destination readme.
cat ${RM_TOC} ${RM_HEADER} ${RM_USAGE} ${RM_FOOTER} > ${RM_FINAL}