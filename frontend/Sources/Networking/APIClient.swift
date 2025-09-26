import Foundation

struct OpportunityDTO: Codable, Identifiable {
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

struct BookLineDTO: Codable {
    let bookmaker: String
    let market: String
    let side: String
    let american_odds: Int?
    let decimal_odds: Double?
    let point: Double?
    let fair_probability: Double?
    let fair_decimal_odds: Double?
}

struct EventLinesDTO: Codable, Identifiable {
    var id: String { event_id }
    let sport: String
    let event_id: String
    let title: String
    let lines: [BookLineDTO]
}

final class APIClient {
    let baseURL: URL

    init(baseURL: URL = URL(string: "http://localhost:8000")!) {
        self.baseURL = baseURL
    }

    func fetchOpportunities() async throws -> [OpportunityDTO] {
        let url = baseURL.appendingPathComponent("api/opportunities")
        let (data, response) = try await URLSession.shared.data(from: url)
        guard let http = response as? HTTPURLResponse, (200...299).contains(http.statusCode) else {
            throw URLError(.badServerResponse)
        }
        return try JSONDecoder().decode([OpportunityDTO].self, from: data)
    }

    func fetchOdds(for sport: String) async throws -> [EventLinesDTO] {
        let url = baseURL.appendingPathComponent("api/odds/\(sport)")
        let (data, response) = try await URLSession.shared.data(from: url)
        guard let http = response as? HTTPURLResponse, (200...299).contains(http.statusCode) else {
            throw URLError(.badServerResponse)
        }
        return try JSONDecoder().decode([EventLinesDTO].self, from: data)
    }
}
