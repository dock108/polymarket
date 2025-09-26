import Foundation

enum Formatters {
    static func percent(_ value: Double?, digits: Int = 2, defaultText: String = "-") -> String {
        guard let v = value else { return defaultText }
        return String(format: "%0.*f%%", digits, v * 100)
    }

    static func decimal(_ value: Double?, digits: Int = 3, defaultText: String = "-") -> String {
        guard let v = value else { return defaultText }
        return String(format: "%0.*f", digits, v)
    }

    static func isoDateTime(_ iso: String?, defaultText: String = "-") -> String {
        guard let iso, let date = ISO8601DateFormatter().date(from: iso) else { return defaultText }
        let fmt = DateFormatter()
        fmt.dateStyle = .medium
        fmt.timeStyle = .short
        return fmt.string(from: date)
    }
}
