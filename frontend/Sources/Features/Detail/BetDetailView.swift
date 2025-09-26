import SwiftUI

struct BetDetailView: View {
    @StateObject var vm: BetDetailViewModel

    init(opportunity: Opportunity) {
        _vm = StateObject(wrappedValue: BetDetailViewModel(opportunity: opportunity))
    }

    var body: some View {
        Form {
            Section(header: Text("Overview")) {
                Text(vm.opportunity.title)
                HStack {
                    Label("EV", systemImage: "percent")
                    Spacer()
                    Text(Formatters.percent(vm.opportunity.ev_percent))
                }
                HStack {
                    Text("Price")
                    Spacer()
                    Text(Formatters.decimal(vm.opportunity.price))
                }
                HStack {
                    Text("P_yes")
                    Spacer()
                    Text(Formatters.decimal(vm.opportunity.yes_probability))
                }
                HStack {
                    Text("Updated")
                    Spacer()
                    Text(Formatters.isoDateTime(vm.opportunity.updated_at))
                }
            }
        }
        .navigationTitle("Bet Detail")
    }
}
