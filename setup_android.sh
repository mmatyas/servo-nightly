#! /bin/sh

# Android SDK
curl -L https://raw.github.com/embarkmobile/android-sdk-installer/version-2/android-sdk-installer | bash /dev/stdin --install=build-tools-23.0.1,android-18
source ~/.android-sdk-installer/env

# Android NDK
wget http://dl.google.com/android/ndk/android-ndk-r10e-linux-x86_64.bin
chmod +x ./android-ndk-r10e-linux-x86_64.bin
./android-ndk-r10e-linux-x86_64.bin > /dev/null

export ANDROID_SDK=$ANDROID_HOME
export ANDROID_NDK=$(pwd)/android-ndk-r10e
export ANDROID_TOOLCHAIN=$(pwd)/ndk-toolchain

mkdir $ANDROID_TOOLCHAIN
$ANDROID_NDK/build/tools/make-standalone-toolchain.sh --platform="android-18" --toolchain=arm-linux-androideabi-4.8 --install-dir=$ANDROID_TOOLCHAIN --ndk-dir=$ANDROID_NDK --arch=arm

export PATH="$PATH:$ANDROID_TOOLCHAIN/bin"
