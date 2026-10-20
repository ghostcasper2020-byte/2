#!/usr/bin/env python3
"""Add a user-owned quick GPS panel to the pinned PersonalGPS/TLocation UI.

This patch does not touch third-party applications, location integrity APIs,
remote pairing, DDI, or the location-simulation service implementation.
"""
from __future__ import annotations

import argparse
from pathlib import Path

SIGNATURE = "// PersonalGPS Quick Panel v0.5 — UI-only extension"

QUICK_PANEL_SWIFT = r'''

// PersonalGPS Quick Panel v0.5 — UI-only extension
// Reuses the application's existing location simulation notifications.
// It does not patch or inject into other applications.
private struct PersonalGPSQuickPanel: View {
    @Environment(\.dismiss) private var dismiss
    let onSimulate: (Double, Double) -> Void
    let onRestore: () -> Void

    @State private var latitudeText = UserDefaults.standard.string(forKey: "PersonalGPS.Quick.Latitude") ?? "24.713600"
    @State private var longitudeText = UserDefaults.standard.string(forKey: "PersonalGPS.Quick.Longitude") ?? "46.675300"
    @State private var mapPosition: MapCameraPosition = .region(
        MKCoordinateRegion(
            center: CLLocationCoordinate2D(latitude: 24.7136, longitude: 46.6753),
            span: MKCoordinateSpan(latitudeDelta: 0.045, longitudeDelta: 0.045)
        )
    )

    private var selectedCoordinate: CLLocationCoordinate2D? {
        guard let lat = Double(latitudeText.trimmingCharacters(in: .whitespacesAndNewlines)),
              let lon = Double(longitudeText.trimmingCharacters(in: .whitespacesAndNewlines)),
              lat.isFinite, lon.isFinite,
              (-90.0 ... 90.0).contains(lat), (-180.0 ... 180.0).contains(lon) else {
            return nil
        }
        return CLLocationCoordinate2D(latitude: lat, longitude: lon)
    }

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 16) {
                    Label("Quick GPS Controls", systemImage: "location.circle.fill")
                        .font(.title3.bold())
                    Text("Tap a point on the map, or enter coordinates. Changes are applied only after you press Set Simulated GPS.")
                        .font(.footnote)
                        .foregroundStyle(.secondary)

                    MapReader { reader in
                        Map(position: $mapPosition) {
                            if let selectedCoordinate {
                                Marker("Selected", coordinate: selectedCoordinate)
                                    .tint(.blue)
                            }
                        }
                        .onTapGesture { screenPoint in
                            guard let coordinate = reader.convert(screenPoint, from: .local) else { return }
                            latitudeText = String(format: "%.6f", coordinate.latitude)
                            longitudeText = String(format: "%.6f", coordinate.longitude)
                        }
                    }
                    .frame(height: 245)
                    .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
                    .accessibilityLabel("Map: tap to pick a simulated location")

                    HStack(spacing: 10) {
                        VStack(alignment: .leading, spacing: 5) {
                            Text("Latitude")
                                .font(.caption)
                            TextField("-90 to 90", text: $latitudeText)
                                .keyboardType(.numbersAndPunctuation)
                                .textFieldStyle(.roundedBorder)
                                .accessibilityIdentifier("quick-gps-latitude")
                        }
                        VStack(alignment: .leading, spacing: 5) {
                            Text("Longitude")
                                .font(.caption)
                            TextField("-180 to 180", text: $longitudeText)
                                .keyboardType(.numbersAndPunctuation)
                                .textFieldStyle(.roundedBorder)
                                .accessibilityIdentifier("quick-gps-longitude")
                        }
                    }

                    if selectedCoordinate == nil {
                        Label("Enter valid latitude and longitude values.", systemImage: "exclamationmark.triangle")
                            .font(.caption)
                            .foregroundStyle(.orange)
                    }

                    Button {
                        guard let point = selectedCoordinate else { return }
                        UserDefaults.standard.set(latitudeText, forKey: "PersonalGPS.Quick.Latitude")
                        UserDefaults.standard.set(longitudeText, forKey: "PersonalGPS.Quick.Longitude")
                        dismiss()
                        onSimulate(point.latitude, point.longitude)
                    } label: {
                        Label("Set Simulated GPS", systemImage: "mappin.and.ellipse")
                            .frame(maxWidth: .infinity)
                    }
                    .buttonStyle(.borderedProminent)
                    .controlSize(.large)
                    .disabled(selectedCoordinate == nil)
                    .accessibilityIdentifier("quick-gps-set")

                    Button(role: .destructive) {
                        dismiss()
                        onRestore()
                    } label: {
                        Label("Return to Real Location", systemImage: "location.slash")
                            .frame(maxWidth: .infinity)
                    }
                    .buttonStyle(.bordered)
                    .controlSize(.large)
                    .accessibilityIdentifier("quick-gps-restore")

                    Text("This controls the existing PersonalGPS developer simulation session. Other apps may detect simulated location. It does not change your IP address or bypass app location verification.")
                        .font(.caption2)
                        .foregroundStyle(.secondary)
                }
                .padding(18)
            }
            .navigationTitle("PersonalGPS")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Done") { dismiss() }
                }
            }
            .onAppear {
                if let point = selectedCoordinate {
                    mapPosition = .region(MKCoordinateRegion(
                        center: point,
                        span: MKCoordinateSpan(latitudeDelta: 0.045, longitudeDelta: 0.045)
                    ))
                }
            }
        }
        .presentationDetents([.large])
    }
}
'''


def patch_source(project_root: Path) -> Path:
    source = project_root / "TLocation" / "Views" / "RootView.swift"
    if not source.is_file():
        raise FileNotFoundError(source)
    text = source.read_text(encoding="utf-8")
    if SIGNATURE in text:
        raise ValueError("Quick Panel is already installed; refusing to apply twice")

    replacements = [
        (
            "import SwiftUI\nimport UIKit\n",
            "import SwiftUI\nimport UIKit\nimport MapKit\n",
        ),
        (
            "    @State private var isShowingSettings = false\n",
            "    @State private var isShowingSettings = false\n"
            "    @State private var isShowingQuickGPSPanel = false\n",
        ),
        (
            "            .animation(.easeInOut(duration: 0.2), value: isReady)\n",
            """            .overlay(alignment: .topLeading) {
                if isReady && !isShowingExpiryWarning {
                    Text("PersonalGPS · Hold for GPS")
                        .font(.caption.weight(.semibold))
                        .padding(.horizontal, 12)
                        .padding(.vertical, 9)
                        .background(.regularMaterial, in: Capsule())
                        .padding(.leading, 16)
                        .padding(.top, 10)
                        .contentShape(Capsule())
                        .onTapGesture { isShowingQuickGPSPanel = true }
                        .onLongPressGesture(minimumDuration: 0.65) {
                            UIImpactFeedbackGenerator(style: .light).impactOccurred()
                            isShowingQuickGPSPanel = true
                        }
                        .accessibilityAddTraits(.isButton)
                        .accessibilityHint("Touch and hold to open the GPS controls")
                        .accessibilityIdentifier("personal-gps-quick-trigger")
                }
            }
            .animation(.easeInOut(duration: 0.2), value: isReady)
""",
        ),
        (
            """        .sheet(isPresented: $isShowingSettings) {
            SettingsView()
        }
""",
            """        .sheet(isPresented: $isShowingSettings) {
            SettingsView()
        }
        .sheet(isPresented: $isShowingQuickGPSPanel) {
            PersonalGPSQuickPanel(onSimulate: { lat, lon in
                LocationSimulationRequest.postSimulate(latitude: lat, longitude: lon)
            }, onRestore: {
                LocationSimulationRequest.postClear()
            })
        }
""",
        ),
    ]
    for old, new in replacements:
        count = text.count(old)
        if count != 1:
            raise ValueError(f"Pinned upstream UI mismatch: expected 1 anchor, found {count}: {old[:65]!r}")
        text = text.replace(old, new, 1)
    text += QUICK_PANEL_SWIFT
    source.write_text(text, encoding="utf-8")
    print("Patched user-owned PersonalGPS UI with the long-press quick panel.")
    print("Existing map simulation, restore, pairing, DDI, and VPN engine remain unchanged.")
    return source


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("upstream", type=Path)
    args = parser.parse_args()
    patch_source(args.upstream)


if __name__ == "__main__":
    main()
