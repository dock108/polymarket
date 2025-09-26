import Foundation

struct BookLine: Codable {
    let bookmaker: String
    let market: String
    let side: String
    let american_odds: Int?
    let decimal_odds: Double?
    let point: Double?
    let fair_probability: Double?
    let fair_decimal_odds: Double?
}

struct EventLines: Codable, Identifiable {
    var id: String { event_id }
    let sport: String
    let event_id: String
    let title: String
    let lines: [BookLine]
}
