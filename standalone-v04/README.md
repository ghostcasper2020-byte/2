# PersonalGPS v0.4 — standalone experimental iPhone build

**Status: build recipe, not a prebuilt IPA.** The included GitHub Actions workflow
fetches a **pinned** open-source on-device location engine, renames its app label
`PersonalGPS`, assigns an independent bundle ID, compiles an **unsigned IPA** on a
macOS GitHub runner, and packages the corresponding AGPL-3.0 source code.

## Very important: 5G-only is not supported reliably

On an unmodified iPhone running **iOS 26**, the currently documented TLocation
method needs the device to be **joined to a Wi-Fi network when initiating
simulation**. Internet through that Wi-Fi network is *not* necessary. Merely
turning on the iPhone's own Personal Hotspot does not meet the requirement.

**A successful IPA build does not prove cellular-only GPS simulation.** No reliable
implementation exists in this package for starting a new GPS simulation over only
5G with Wi-Fi disabled. Once initiated while on Wi-Fi, an existing simulated
location might survive a network change for a time, but this is not guaranteed.

Do not use this prototype for safety, navigation, emergency calls, regulatory
compliance, attendance, or applications that rely on verified real-world position.

## How to add to your existing `ghostcasper2020-byte/1` GitHub repository

Keep your existing v0.3 project. You do **not** need to delete or replace its
`.github/workflows/build-unsigned-ipa.yml` workflow.

1. Extract this ZIP on Windows.
2. Copy its `.github/workflows/build-personalgps-v04.yml` into the **same path**
   of your existing GitHub repository (including the leading dot in `.github`).
3. Copy the entire `standalone-v04/` directory into the **repository root**.
4. Commit the new files, keeping both v0.3 and v0.4 workflows.
5. GitHub → **Actions** → **Build PersonalGPS v0.4 on-device (experimental)**
   → **Run workflow** → `main` → **Run workflow**.
6. A successful run produces an artifact ZIP containing
   `PersonalGPS-v0.4-unsigned.ipa` and
   `PersonalGPS-v0.4-corresponding-source.zip`.
7. Extract the ZIP. Sign/install the unsigned IPA using the Windows signing
   process (for example, Sideloadly) that worked for your v0.3 IPA.

This v0.4 IPA has a separate bundle identifier, so v0.3 can remain installed.
The new app's screen is derived from TLocation, **not** a direct continuation of
v0.3's PC-server interface. The original TLocation app icon may remain.

## First-time setup on iOS 26 (requires a Windows PC one time)

1. Keep the phone **unlocked and trusted** over USB.
2. Generate the phone's `.mobiledevicepairing` credentials using a reputable,
   compatible pairing tool such as the JitterbugPair or the StikDebug pairing
   workflow. See official project guides below.
3. Transfer that file privately to the iPhone Files app. **NEVER upload it to
   GitHub, post screenshots of its contents, or share it with third parties.**
4. Install and connect **LocalDevVPN** on iPhone:
   https://apps.apple.com/us/app/localdevvpn/id6755608044
5. **Join an actual Wi-Fi network temporarily.** It can lack internet. The
   iPhone's Personal Hotspot used to connect a Windows PC is *not* equivalent.
6. Open the installed PersonalGPS standalone build and import the pairing file.
   Follow the app's pairing/VPN instructions and wait until the connection and
   Developer Disk Image are reported ready.
7. Pick a map location and press the app's simulation control. Validate results
   using Apple Maps and use the app's clear/restore control when finished.

### Cellular-only experiment (not a supported feature)

After you have tested that a simulation works *while joined to Wi-Fi*:

- Clear the simulated GPS, turn Wi-Fi off, leave cellular 5G enabled, and try to
  re-establish the local VPN/device connection and start a new simulation.
- **Expect this to fail on recent iOS releases.** Record the exact error; do not
  confuse a moving map pin with actual system-wide simulation.
- Alternatively, while actively simulating over Wi-Fi, disconnect from Wi-Fi and
  observe whether the location persists. If the session drops, clear/reset GPS.

None of these steps provides undetectable spoofing. Third-party applications can
check `CLLocation.sourceInformation.isSimulatedBySoftware` and other signals.

## Common problems

- **Build fails:** Open the failed step in GitHub Actions. The repo is pinned
  to an upstream commit to avoid silent changes. Changes in runner/Xcode may
  still require build adjustments. No macOS build or device test was run by
  the author of this recipe.
- **Pairing invalid:** Re-pair with your own unlocked device. OS upgrades and
  resets can invalidate pairing credentials.
- **Tunnel unavailable over cellular:** Expected; Wi-Fi association is a known
  prerequisite of this particular engine.
- **App installs but does not simulate:** A valid signature alone doesn't
  establish the loopback developer connection. Verify VPN, pairing, Developer
  Mode, DDI, and the actual simulation in Apple Maps.
- **Sideload provisioning issues:** Your signing tool/account must support
  the required binary and entitlements. Nothing is guaranteed by an unsigned
  IPA alone. Free-account signing typically needs refreshing after seven days.

## References

- TLocation (upstream and Wi-Fi limits): https://github.com/truongkma/t-location
- StikDebug: https://github.com/StikDebug/StikDebug
- StikDebug pairing-file guide: https://github.com/StikDebug/StikDebug-Guide/blob/main/pairing_file.md
- LocalDevVPN: https://apps.apple.com/us/app/localdevvpn/id6755608044
- Apple simulation-source flag: https://developer.apple.com/documentation/corelocation/cllocationsourceinformation/issimulatedbysoftware

See NOTICE.md for source authorship and AGPL-3.0 obligations.
