import SwiftUI

struct AllSportsView: View {
    @StateObject private var vm = AllSportsViewModel()
    @ObservedObject private var settings = SettingsStore.shared

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
                        NavigationLink(destination: BetDetailView(opportunity: opp)) {
                            VStack(alignment: .leading, spacing: 4) {
                                HStack {
                                    Text(opp.title).font(.headline)
                                    if let basis = opp.comparison_basis, basis == "none" {
                                        Text("No comparison")
                                            .font(.caption2)
                                            .padding(.horizontal, 6)
                                            .padding(.vertical, 2)
                                            .background(Color.gray.opacity(0.2))
                                            .cornerRadius(4)
                                    } else if let basis = opp.comparison_basis {
                                        Text(basis)
                                            .font(.caption2)
                                            .padding(.horizontal, 6)
                                            .padding(.vertical, 2)
                                            .background(Color.blue.opacity(0.15))
                                            .cornerRadius(4)
                                    }
                                }
                                HStack(spacing: 10) {
                                    if let sport = opp.sport { Text(sport).font(.caption).foregroundColor(.secondary) }
                                    if let ev = opp.ev_percent { Text(String(format: "EV %%: %.2f", ev)).font(.subheadline) }
                                    if let price = opp.price { Text(String(format: "Price: %.3f", price)).font(.subheadline) }
                                    if let prob = opp.yes_probability { Text(String(format: "P_yes: %.3f", prob)).font(.subheadline) }
                                    if let stale = opp.is_stale, stale {
                                        Text("Stale")
                                            .font(.caption2)
                                            .foregroundColor(.orange)
                                    }
                                }
                                .foregroundColor(.secondary)

                                if settings.developerMode {
                                    VStack(alignment: .leading, spacing: 2) {
                                        HStack {
                                            Text("IDs:")
                                            Text("event=\(opp.event_id ?? "-") market=\(opp.market_id ?? "-")")
                                        }
                                        .font(.caption2)
                                        .foregroundColor(.secondary)

                                        HStack {
                                            Text("Updated:")
                                            Text(Formatters.isoDateTime(opp.updated_at))
                                        }
                                        .font(.caption2)
                                        .foregroundColor(.secondary)
                                    }
                                }
                            }
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
                        ForEach(vm.availableSports, id: \.self) { s in
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
