# SCR01 AVK2 callback compatibility

This workaround addresses [upstream issue #814](https://github.com/Mygod/VPNHotspot/issues/814)
on Samsung SCR01, Android 11 / API 30, fingerprint containing `SCR01KDU1AVK2`.
Other devices, Android versions, and firmware fingerprints retain the original behavior.

## Failure and source changes

Samsung's `registerTetheringEventCallback` attempts to write `MHS_DMZ_ENABLED` via the
settings provider. On the verified firmware registration can throw a `SecurityException`
mentioning `WRITE_SETTINGS`, or an `IllegalArgumentException` mentioning `secure settings`.
The root `app_process` additionally fails to acquire the settings provider because its
`IApplicationThread` has no ActivityManager process record.

`TetherStates` uses its existing sticky-broadcast owner on this firmware, including the
existing receiver-unregistration and pending-dispatch cleanup. Each `eventFlow` collector
records whether its callback registration returned normally. Only the verified setting
failures are logged and tolerated; cleanup unregisters only successfully registered callbacks.
The extra caller/provider failure requires UID 0 and both the exact caller-message prefix
and the settings-provider suffix. Other permissions, providers, exception types, and all
failures on other firmware still propagate.

This fallback does not recreate every callback event. Callback-only client/offload/upstream
notifications are unavailable to a collector whose registration was rejected; tether-state
broadcasts and the existing interface monitoring continue. No additional `WRITE_SETTINGS`
permission, settings-provider spoofing, routing mutation, hidden API, or daemon change is added.
No daemon documentation update is needed because daemon ownership and routing are unchanged.

## Proven APK repair versus source port

The device-tested APK was produced from the official **v3.0.8 ARM64 release** with the
three exact smali transforms in [`scripts/scr01-compat3`](../scripts/scr01-compat3).
The source changes in this repository express the same device/exception gates in the
current Kotlin callback-flow lifecycle. They are a source port, not a claim that a new
full application build was installed on the device.

Original APK:

- URL: `https://github.com/Mygod/VPNHotspot/releases/download/v3.0.8/mobile-arm64-v8a-release.apk`
- SHA-256: `c71b1c9170235fa6a271e1617ab343767ebafe638a1833c3ff20733ef5861668`
- Tested compat3 APK SHA-256: `f2f99d47a47bf146f74f0c9b1f3f70b682f8f88e3c9cd17fb188bf815290004b`

For exact repair reproduction, place the official APK at
`scripts/scr01-compat3/original.apk`, set `APKTOOL_JAR` to an absolute Apktool 3.0.2 JAR path,
and run `scripts/scr01-compat3/rebuild.sh`. `patch.py` verifies the official APK digest;
all three transforms verify the expected instruction shapes. The result is unsigned.
Use Android build-tools `zipalign` and `apksigner` with your own signing key. A different
certificate cannot update an existing installation signed by another key.

The private signing material used for the device build is intentionally not part of the
repository. APKs, decoded vendor/framework files, device preferences, screenshots, network
names, device serial numbers, and raw logs are not included.

## Validation

- Device-tested smali repair: the actual helper passed 9 exception cases plus 18 cleanup
  checks in both ordinary-shell and root contexts. The client list opened without the
  reported settings-provider toast. Native assets and resources were unchanged.
- Source port: `Scr01CallbackCompatTest` covers the firmware gate, known settings failures,
  unexpected exception types, null messages, root-only matching, and wrong provider/prefix.
  Three JUnit tests passed against the actual Java helper with Android SDK stubs.
- `./gradlew :mobile:compileDebugKotlin :mobile:testDebugUnitTest --offline --no-daemon`
  was attempted with an isolated cache. It stopped before compilation because the Gradle
  settings plugin `io.github.ben-manes.versions.settings:0.58.0` was not cached.
  This machine also has Android SDK 34 rather than the project's required compile SDK 37.
  Full Kotlin/app compilation therefore remains unverified; passing the three Java tests
  is not a claim that the whole app builds.

The Wi-Fi relay KernelSU module belongs to the separate SCR01 tools collection; this
callback repair does not enable STA/AP concurrency or change the hotspot channel.
