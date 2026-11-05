#!/bin/sh
set -eu
cd "$(dirname "$0")"
: "${APKTOOL_JAR:?Set APKTOOL_JAR to Apktool 3.0.2}"
[ -f original.apk ] || { echo 'Place the official v3.0.8 ARM64 APK at scripts/scr01-compat3/original.apk'; exit 1; }
[ ! -e decoded ] || { echo 'decoded already exists; use a fresh working directory.'; exit 1; }
java -jar "$APKTOOL_JAR" d -r -o decoded original.apk
python3 patch.py
python3 patch2.py
python3 patch3.py
java -jar "$APKTOOL_JAR" b decoded -o unsigned.apk
echo 'unsigned.apk created. Zipalign and sign with your own local key before installation.'
