import Foundation
import Combine

final class AllSportsViewModel: ObservableObject {
    @Published var allOpportunities: [Opportunity] = []
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?

    @Published var selectedSport: String? = nil // nil = All
    @Published var minEVPercent: Double = 0 // 0 disables EV filtering in beta

    @Published var visibleCount: Int = 50

    private let api: APIClient

    init(api: APIClient = APIClient()) {
        self.api = api
    }

    var availableSports: [String] {
        let sports = Set(allOpportunities.compactMap { $0.sport }).sorted()
        return ["All"] + sports
    }

    var filteredSorted: [Opportunity] {
        let threshold = minEVPercent / 100.0
        let sportFilter = selectedSport == nil || selectedSport == "All" ? nil : selectedSport
        let shouldFilterEV = threshold > 0
        let filtered = allOpportunities.filter { opp in
            let sportOk = sportFilter == nil ? true : (opp.sport == sportFilter!)
            let evOk = !shouldFilterEV || ((opp.ev_percent ?? -Double.infinity) >= threshold)
            return sportOk && evOk
        }
        .sorted { (lhs, rhs) in
            (lhs.ev_percent ?? -Double.infinity) > (rhs.ev_percent ?? -Double.infinity)
        }
        if filtered.count <= visibleCount { return filtered }
        return Array(filtered.prefix(visibleCount))
    }

    @MainActor
    func load() async {
        isLoading = true
        errorMessage = nil
        do {
            let data = try await api.fetchOpportunities()
            allOpportunities = data
        } catch {
            errorMessage = error.localizedDescription
        }
        isLoading = false
    }

    func loadMoreIfNeeded(currentItem: Opportunity?) {
        guard let currentItem = currentItem else { return }
        let items = filteredSorted
        if let index = items.firstIndex(where: { $0.id == currentItem.id }), index >= items.count - 10 {
            visibleCount = min(visibleCount + 50, 1000)
        }
    }
}
