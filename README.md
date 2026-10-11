# 🛠️ Free Tool Scout (24/7 Automation)

Autonomous 24/7 scout running on GitHub Actions and OpenMausBot to discover trending open-source utilities, developer CLI tools, AI frameworks, and automation apps.

## 🚀 How It Works
- **GitHub Actions (24/7 Cloud)**: Runs automatically every 6 hours via `.github/workflows/scout.yml`. Queries GitHub APIs for newly starred and trending open-source projects across key categories.
- **Continuous Logging**: Automatically updates [`DISCOVERED_TOOLS.md`](./DISCOVERED_TOOLS.md) and maintains [`tools_database.json`](./tools_database.json) to prevent duplicate reports.
- **OpenMausBot Local Sync**: Hermes syncs with this repository to inform you in real-time when game-changing tools are discovered.

## 📂 Discovered Tools Catalog
Browse the complete catalog of tools in [**DISCOVERED_TOOLS.md**](./DISCOVERED_TOOLS.md).
