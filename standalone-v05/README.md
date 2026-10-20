# PersonalGPS v0.5 — Long-Press Quick GPS Panel

This is a **patch/build recipe**, not a signed IPA. It builds on your working PersonalGPS v0.4 standalone project in GitHub repository `ghostcasper2020-byte/2`.

**What changes:** A small `PersonalGPS · Hold for GPS` capsule appears near the top left **inside PersonalGPS only**. Tap or long press (~0.65 seconds) to open the Quick GPS Controls panel. Choose a point on an interactive map, enter latitude/longitude, start the existing PersonalGPS simulation, or restore your real location. The panel remembers your last chosen coordinates.

**What does not change:** The existing TLocation/StikDebug-derived engine, LocalDevVPN, pairing file requirements, iOS 26 Wi-Fi association limitation, and detection by other applications. The panel is **not an overlay inside Ma'an** and does not modify or bypass any attendance/location verification checks.

## Upgrade your existing GitHub repository

You already have the v0.4 files in repository `ghostcasper2020-byte/2`. **Keep them.** Add only these new items to the repository **root**:

```text
.github/
  workflows/
    build-personalgps-v05.yml    <-- KEEP the initial dot in .github
standalone-v05/
  README.md
  patch_quick_panel.py
  tests/
    test_patch.py
```

The ZIP includes a root `README.md`, but your existing GitHub README does not need to be replaced.

1. Extract the ZIP on Windows.
2. Upload the `standalone-v05` folder to the **root** of your existing GitHub repository.
3. Copy `.github/workflows/build-personalgps-v05.yml` to that same path in GitHub. Use Add file -> Create new file if the hidden `.github` directory is difficult to drag from Windows.
4. Open **GitHub → Actions → Build PersonalGPS v0.5 Quick Panel (experimental) → Run workflow → main**.
5. Download its artifact. Extract `PersonalGPS-v0.5-unsigned.ipa`, then sign/install with Sideloadly as you did for v0.4.
6. v0.5 uses the same bundle identifier as v0.4, so it is intended to upgrade/replace v0.4 rather than appear as a third icon. Keep a private backup of your pairing file before replacing any app: installation/signing may affect app data.
7. Open PersonalGPS, ensure pairing and LocalDevVPN are working, then touch and hold the **PersonalGPS · Hold for GPS** capsule. Test changing a location in Apple Maps. Restore actual GPS after testing.

## Technical implementation

- Fetches the same **pinned** TLocation revision as your existing v0.4 workflow.
- Runs your existing v0.4 `standalone-v04/rebrand.py` first.
- Applies a **fail-fast** UI patch to `TLocation/Views/RootView.swift`, without modifying other applications or the on-device pairing/tunnel protocol.
- Reuses `LocationSimulationRequest.postSimulate(...)` and `.postClear()` so the existing map is the single owner of simulation state.
- Validates coordinates (-90..90 latitude, -180..180 longitude), includes a map picker, and keeps last selected coordinates on-device.
- Runs offline Python patch checks and `swiftc -frontend -parse` before Xcode's full device build.
- Packages a corresponding source archive with license/attribution, because upstream TLocation/StikDebug code is AGPL-3.0.

## Important limitations

- This package does **not** contain a compiled IPA. macOS compilation and a real-device test have not been run in this environment.
- On iOS 26, initiating standalone developer location simulation over **5G only** with Wi-Fi completely disconnected remains unverified and may fail. The upstream engine normally needs the iPhone to join a Wi-Fi network to start a session.
- Location simulation can be identified by third-party apps; this version is for using and testing **your own** app, not evading attendance verification.
- Do not upload actual device pairing files, private keys, tokens, or signing credentials to GitHub or to this conversation.

## Source / license

Original on-device engine: [truongkma/t-location](https://github.com/truongkma/t-location), derived from [StikDebug](https://github.com/StikDebug/StikDebug), AGPL-3.0. Pinned commit: `5e57f815e5958f133dfbaae8252473054adeccf0`.
The downloaded build's corresponding-source artifact contains the patched engine source and this patch recipe.
