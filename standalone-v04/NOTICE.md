# PersonalGPS v0.4 experimental — upstream and license notice

The on-device location simulation engine in this experimental package is **not original PersonalGPS code**.
The GitHub workflow downloads the source for **TLocation** by truongkma at an exact commit,
`5e57f815e5958f133dfbaae8252473054adeccf0` (2026-08-18).
TLocation itself is derived from **StikDebug**, with contributions by Stephen Bove (Stik)
and collaborators, and includes **idevice** by jkcoxson and contributors.

- https://github.com/truongkma/t-location
- https://github.com/StikDebug/StikDebug
- https://github.com/jkcoxson/idevice

TLocation is licensed under **AGPL-3.0**. Its LICENSE and upstream notices remain intact.
Any redistributed derivative must comply with the applicable license, including source
availability obligations. This workflow also packages the complete corresponding
modified upstream source together with this rebranding script.

The modifications are limited to the app's displayed name and unique bundle identifier.
No iOS exploit, cellular-only bypass, anti-detection functionality, or private credential
extraction is implemented.
