#!/bin/bash

_pwd=$(pwd)
script_path=$(realpath $(dirname $0))

echo "cd ${script_path}"
cd ${script_path}

test_dirs=(analyze/dataset analyze/dft_equiv analyze/error compute/eigen convert/abacus convert/deeph convert/fhi_aims convert/hopcp convert/openmx convert/siesta)

for test_dir in ${test_dirs[@]}; do
    cd ${test_dir}
    for d1 in $(/bin/ls .); do
        if [[ "$d1" == *.sh ]]; then
            continue
        elif [[ "$d1" == *.clean ]]; then
            continue
        elif [[ "$d1" == *.bak ]]; then
            continue
        elif [[ "$d1" == *.ipynb ]]; then
            continue
        elif [[ "$d1" == *install ]]; then
            continue
        else
            read -p "rm -r ${test_dir}/${d1} ? [y/N]" REPLY
            if [[ "$REPLY" == "y" ]]; then
                rm -r ${d1}
            fi
        fi
    done
    cd ${script_path}
done

echo "cd ${_pwd}"
cd ${_pwd}
