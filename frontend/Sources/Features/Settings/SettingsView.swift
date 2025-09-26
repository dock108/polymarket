import SwiftUI

struct SettingsView: View {
    @AppStorage("fee_cushion") var feeCushion: Double = 0.025
    @AppStorage("refresh_interval") var refreshInterval: Double = 600

    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Modeling")) {
                    HStack {
                        Text("Fee Cushion")
                        Spacer()
                        Text(String(format: "%.3f", feeCushion))
                    }
                    Slider(value: $feeCushion, in: 0...0.1, step: 0.001)
                }
                Section(header: Text("Refresh")) {
                    Stepper(value: $refreshInterval, in: 60...3600, step: 60) {
                        Text("Interval: \(Int(refreshInterval))s")
                    }
                }
            }
            .navigationTitle("Settings")
        }
    }
}
