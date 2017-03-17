#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )
cd "$parent_path"
cd ../

while :
    do
        python -m backup.ServiceStart
        sleep 1.5
done
