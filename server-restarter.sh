#!/bin/bash

SERVERS=(pub1 pub2 pub3)

# This script is meant to work with QLDS Manager and default QL settings
# It stops, updates and starts servers one by one
# Just add server's ids to array above
# Feel free to adjust the script to your needs

ABSOLUTE_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for sv in ${SERVERS[*]}
do
    qldsmanager server stop "$sv" && \
    python3 "$ABSOLUTE_PATH/qlcfg.py" \
    --access \
    "~/.quakelive/$sv/baseq3/access.txt" \
    --remove \
    --workshop \
    "~/.quakelive/$sv/baseq3/workshop.txt"
done


python3 "$ABSOLUTE_PATH/qlcfg.py" --steamcmd


for sv in ${SERVERS[*]}
do
    qldsmanager server start "$sv"
done