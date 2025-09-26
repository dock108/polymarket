import Foundation

struct Opportunity: Codable, Identifiable {
    let id: String
    let source: String
    let title: String
    let sport: String?
    let event_id: String?
    let market_id: String?
    let yes_probability: Double?
    let price: Double?
    let ev_usd_per_share: Double?
    let ev_percent: Double?
    let updated_at: String?
}
