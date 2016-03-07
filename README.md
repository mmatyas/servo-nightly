
# servo-nightly

[![Build Status](https://travis-ci.org/mmatyas/servo-nightly.svg)](https://travis-ci.org/mmatyas/servo-nightly), nightly builds [here](https://github.com/mmatyas/servo-nightly/releases)

This repo contains my scripts for automatic build testing on Travis.

- `update_servo.sh`: runs locally, updates or pulls the latest Servo in `./servo`
- `update_tags.py`: runs locally, creates and uploads a new Git tag, which triggers the Travis build. Combine with `update_servo.sh`. Requires `GITHUB_TOKEN` to be set.
- `setup_android.sh`: sets up Android SDK and NDK on Travis
- `upload_to_github.py`: if the build is successful, uploads `./servo/$ASSET_NAME` to GitHub for the latest tag. Requires `GITHUB_TOKEN` to be set.

Interested in cross-compiling Servo? Here is a short guide for ARM and AArch64: [mmatyas.github.io/blog/servo-short-cross-compilation-guide](https://mmatyas.github.io/blog/servo-short-cross-compilation-guide)
