#!/usr/bin/env bash
# Build the Android app (debug APK) from index.html.
#   PY=<python with Pillow> ./build_app.sh
# Output: roadkill-protocol.apk
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-python3}
export JAVA_HOME=${JAVA_HOME:-$HOME/tools/jdk17}
SDK=${ANDROID_HOME:-$HOME/Android/Sdk}

"$PY" build.py --app
rm -rf android/app/src/main/assets/www
mkdir -p android/app/src/main/assets
cp -r dist-app android/app/src/main/assets/www
rm -f android/app/src/main/assets/www/.nojekyll android/app/src/main/assets/www/manifest.webmanifest
"$PY" android/make_icons.py
[ -f android/local.properties ] || echo "sdk.dir=$SDK" > android/local.properties
(cd android && ./gradlew --no-daemon -q assembleDebug)
cp android/app/build/outputs/apk/debug/app-debug.apk roadkill-protocol.apk
echo "built $(pwd)/roadkill-protocol.apk ($(du -h roadkill-protocol.apk | cut -f1))"
