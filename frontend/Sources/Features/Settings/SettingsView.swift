import SwiftUI

struct SettingsView: View {
    @StateObject private var store = SettingsStore.shared

    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Modeling")) {
                    HStack {
                        Text("Fee Cushion")
                        Spacer()
                        Text(String(format: "%.3f", store.feeCushion))
                    }
                    Slider(value: $store.feeCushion, in: 0...0.1, step: 0.001)

                    HStack {
                        Text("Default EV Threshold")
                        Spacer()
                        Text(String(format: "%.0f%%", store.defaultEVPercent))
                    }
                    Slider(value: $store.defaultEVPercent, in: 0...50, step: 1)
                }

                Section(header: Text("Refresh")) {
                    Stepper(value: $store.refreshIntervalSeconds, in: 60...3600, step: 60) {
                        Text("Interval: \(Int(store.refreshIntervalSeconds))s")
                    }
                }

                Section(header: Text("Developer")) {
                    Toggle("Developer Mode", isOn: $store.developerMode)
                        .tint(.accentColor)
                    Text("Shows raw opportunities and extra fields in beta.")
                        .font(.footnote)
                        .foregroundColor(.secondary)
                }
            }
            .navigationTitle("Settings")
        }
    }
}
