import Foundation
import Combine

final class SettingsStore: ObservableObject {
    static let shared = SettingsStore()

    private let defaults = UserDefaults.standard

    private enum Keys {
        static let feeCushion = "fee_cushion"
        static let refreshInterval = "refresh_interval"
        static let defaultEVPercent = "default_ev_percent"
        static let developerMode = "developer_mode"
    }

    @Published var feeCushion: Double {
        didSet { defaults.set(feeCushion, forKey: Keys.feeCushion) }
    }

    @Published var refreshIntervalSeconds: Double {
        didSet { defaults.set(refreshIntervalSeconds, forKey: Keys.refreshInterval) }
    }

    @Published var defaultEVPercent: Double {
        didSet { defaults.set(defaultEVPercent, forKey: Keys.defaultEVPercent) }
    }

    @Published var developerMode: Bool {
        didSet { defaults.set(developerMode, forKey: Keys.developerMode) }
    }

    private init() {
        let fee = defaults.object(forKey: Keys.feeCushion) as? Double ?? 0.025
        let refresh = defaults.object(forKey: Keys.refreshInterval) as? Double ?? 600
        let ev = defaults.object(forKey: Keys.defaultEVPercent) as? Double ?? 0
        let dev = defaults.object(forKey: Keys.developerMode) as? Bool ?? false
        self.feeCushion = fee
        self.refreshIntervalSeconds = refresh
        self.defaultEVPercent = ev
        self.developerMode = dev
    }
}
