import SwiftUI

@main
struct PolymarketEdgeApp: App {
    var body: some Scene {
        WindowGroup {
            RootTabs()
        }
    }
}

struct RootTabs: View {
    var body: some View {
        TabView {
            AllSportsView()
                .tabItem {
                    Image(systemName: "list.bullet.rectangle")
                    Text("All Sports")
                }
            GolfView()
                .tabItem {
                    Image(systemName: "figure.golf")
                    Text("Golf")
                }
            SettingsView()
                .tabItem {
                    Image(systemName: "gearshape")
                    Text("Settings")
                }
        }
    }
}
