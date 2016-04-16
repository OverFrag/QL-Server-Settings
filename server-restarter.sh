#!/bin/bash

SERVERS=(pub1 pub2 pub3)

# This script is meant to work with QLDS Manager and default QL settings
# It stops, updates and starts servers one by one
# Just add server's ids to array above
# Feel free to adjust the script to your needs

for sv in $(SERVERS[*])
do
    echo "qldsmanager server stop $sv" && \
    echo "python3 ~/QL-Server-Settings/qlcfg.py \
    --access \
    ~/.quakelive/$(sv)/baseq3/access.txt \
    --remove \
    --workshop \
    ~/.quakelive/$(sv)/baseq3/workshop.txt" && \
    echo "qldsmanager server start $(sv)"
done
