import SwiftUI

struct AllSportsView: View {
    @State private var opportunities: [Opportunity] = []
    @State private var isLoading: Bool = false
    @State private var errorMessage: String?

    let api = APIClient()

    var body: some View {
        NavigationView {
            Group {
                if let errorMessage = errorMessage {
                    VStack(spacing: 8) {
                        Text("Error: \(errorMessage)").foregroundColor(.red)
                        Button("Retry") { Task { await load() } }
                    }
                } else if isLoading {
                    ProgressView("Loading opportunities…")
                } else if opportunities.isEmpty {
                    Text("No opportunities available right now")
                        .foregroundColor(.secondary)
                } else {
                    List(opportunities) { opp in
                        VStack(alignment: .leading, spacing: 4) {
                            Text(opp.title).font(.headline)
                            HStack {
                                if let ev = opp.ev_percent {
                                    Text(String(format: "EV %%: %.2f", ev * 100))
                                }
                                if let price = opp.price {
                                    Text(String(format: "Price: %.3f", price))
                                }
                                if let prob = opp.yes_probability {
                                    Text(String(format: "P_yes: %.3f", prob))
                                }
                            }
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                        }
                    }
                }
            }
            .navigationTitle("All Sports")
            .task { await load() }
            .refreshable { await load() }
        }
    }

    @MainActor
    private func load() async {
        isLoading = true
        errorMessage = nil
        do {
            let data = try await api.fetchOpportunities()
            opportunities = data
        } catch {
            errorMessage = error.localizedDescription
        }
        isLoading = false
    }
}
