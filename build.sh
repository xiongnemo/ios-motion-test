#!/bin/bash
# MotionTest.ipa, not signed by Apple: for an iOS that installs apps without Apple's signature (the K40 port).
#   macOS:      ./build.sh                      (Xcode's clang and iPhoneOS SDK, through xcrun)
#   elsewhere:  CC=<a clang that targets iOS and links with ld64> SDK=<an iPhoneOS SDK> ./build.sh
#               e.g. CC=xnu-clang SDK=$THEOS/sdks/iPhoneOS16.5.sdk
# OUT=DIR (default build/): DIR/Payload/MotionTest.app and DIR/MotionTest.ipa.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
OUT=${OUT:-$HERE/build}
if [ -z "${SDK:-}" ] && command -v xcrun >/dev/null 2>&1; then
	SDK=$(xcrun --sdk iphoneos --show-sdk-path)
	CC=${CC:-$(xcrun --sdk iphoneos --find clang)}
fi
: "${SDK:?SDK: an iPhoneOS SDK (on macOS xcrun finds it)}"
CC=${CC:-clang}
APP=$OUT/Payload/MotionTest.app

rm -rf "$OUT/Payload" "$OUT/MotionTest.ipa"
mkdir -p "$APP"
# (-target, not -arch and -miphoneos-version-min: a wrapper such as xnu-clang puts its own -target ios16.5 first, which
# wins over -miphoneos-version-min, and the program then asked for iOS 16.5; the last -target is the one that counts)
$CC -target arm64-apple-ios15.0 -isysroot "$SDK" -O1 -fobjc-arc \
	-framework UIKit -framework Foundation -framework CoreMotion -framework CoreGraphics -framework QuartzCore \
	-o "$APP/MotionTest" "$HERE/main.m"
sed 's/\r$//' "$HERE/Info.plist" > "$APP/Info.plist"
python3 -I "$HERE/mkicon.py" "$APP"
printf 'APPL????' > "$APP/PkgInfo"
(cd "$OUT" && python3 -c "import shutil; shutil.make_archive('MotionTest', 'zip', '.', 'Payload')" && mv MotionTest.zip MotionTest.ipa)
ls -l "$OUT/MotionTest.ipa"
