import Foundation

final class BetDetailViewModel: ObservableObject {
    @Published var opportunity: Opportunity

    init(opportunity: Opportunity) {
        self.opportunity = opportunity
    }
}
