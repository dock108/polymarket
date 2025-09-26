import SwiftUI

struct AllSportsView: View {
    @StateObject private var vm = AllSportsViewModel()

    var body: some View {
        NavigationView {
            Group {
                if let errorMessage = vm.errorMessage {
                    VStack(spacing: 8) {
                        Text("Error: \(errorMessage)").foregroundColor(.red)
                        Button("Retry") { Task { await vm.load() } }
                    }
                } else if vm.isLoading {
                    ProgressView("Loading opportunities…")
                } else if vm.filteredSorted.isEmpty {
                    Text("No opportunities match filters")
                        .foregroundColor(.secondary)
                } else {
                    List(vm.filteredSorted) { opp in
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
                        .onAppear { vm.loadMoreIfNeeded(currentItem: opp) }
                    }
                }
            }
            .navigationTitle("All Sports")
            .toolbar {
                ToolbarItemGroup(placement: .navigationBarTrailing) {
                    Picker("Sport", selection: Binding(
                        get: { vm.selectedSport ?? "All" },
                        set: { vm.selectedSport = $0 == "All" ? nil : $0 }
                    )) {
                        ForEach(vm.availableSports, id: \ .self) { s in
                            Text(s)
                        }
                    }
                    .pickerStyle(MenuPickerStyle())

                    HStack(spacing: 6) {
                        Text("EV ≥")
                        Slider(value: Binding(get: { vm.minEVPercent }, set: { vm.minEVPercent = $0 }), in: 0...50, step: 1)
                            .frame(width: 120)
                        Text(String(format: "%.0f%%", vm.minEVPercent))
                            .frame(minWidth: 40, alignment: .trailing)
                    }
                }
            }
            .task { await vm.load() }
            .refreshable { await vm.load() }
        }
    }
}
