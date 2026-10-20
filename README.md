# PersonalGPS v0.4 — experimental on-device engine build recipe

Read **standalone-v04/README.md** before uploading files or building.

This is a **GitHub Actions recipe**, not a compiled or signed IPA. It uses pinned
AGPL-3.0 TLocation/StikDebug-derived code to build a separately installable
on-device location simulator on a macOS runner. It is intentionally distinct
from the old Windows-companion app.

**Limit:** Reliable start of GPS simulation using **5G only, with Wi-Fi disabled,
is not supported** by the upstream method on recent iOS builds. A one-time PC
pairing file and a loopback VPN are needed, and connection to Wi-Fi when starting
simulation is currently required according to the upstream project's guidance.

Do not upload pairing files or device secrets into a repository.
