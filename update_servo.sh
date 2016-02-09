#! /bin/sh

set -o nounset
set -o errexit
set -o xtrace

if [ ! -d ./servo ]; then
    git clone https://github.com/servo/servo.git
fi

cd servo
git pull
cd ..
