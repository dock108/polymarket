import Foundation

final class APIClient {
    let baseURL: URL

    init() {
        if let urlString = Bundle.main.object(forInfoDictionaryKey: "API_BASE_URL") as? String, let url = URL(string: urlString) {
            self.baseURL = url
        } else {
            self.baseURL = URL(string: "http://localhost:8000")!
        }
    }

    func fetchOpportunities() async throws -> [Opportunity] {
        try await request(path: "api/opportunities")
    }

    func fetchOdds(for sport: String) async throws -> [EventLines] {
        try await request(path: "api/odds/\(sport)")
    }

    private func request<T: Decodable>(path: String, retries: Int = 2, delayMs: UInt64 = 300) async throws -> T {
        let url = baseURL.appendingPathComponent(path)
        var lastError: Error?
        var attempt = 0
        while attempt <= retries {
            do {
                var req = URLRequest(url: url)
                req.timeoutInterval = 15
                let (data, response) = try await URLSession.shared.data(for: req)
                guard let http = response as? HTTPURLResponse else { throw URLError(.badServerResponse) }
                guard (200...299).contains(http.statusCode) else { throw URLError(.badServerResponse) }
                return try JSONDecoder().decode(T.self, from: data)
            } catch {
                lastError = error
                if attempt == retries { break }
                try await Task.sleep(nanoseconds: delayMs * 1_000_000)
                attempt += 1
            }
        }
        throw lastError ?? URLError(.unknown)
    }
}
