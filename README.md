
# servo-nightly

[![Build Status](https://travis-ci.org/mmatyas/servo-nightly.svg?branch=master)](https://travis-ci.org/mmatyas/servo-nightly)

This repo contains my scripts for automatic build testing on Travis.

- `update_servo.sh`: runs locally, updates or pulls the latest Servo in `./servo`
- `update_tags.py`: runs locally, creates new GitHub tag which triggers the Travis build; combine with `update_servo.sh`.
- `setup_android.sh`: sets up Android SDK and NDK on Travis
- `upload_to_github.py`: if the build is successful, uploads `./$ASSET_NAME` to GitHub

Interested in cross-compiling Servo? Here is a short guide for ARM and AArch64: [mmatyas.github.io/blog/servo-short-cross-compilation-guide](https://mmatyas.github.io/blog/servo-short-cross-compilation-guide)
