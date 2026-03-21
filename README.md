# Job Sourcing Engine

A professional Python framework designed to aggregate, sanitize, and manage live data from diverse job platforms. This tool automates the discovery process, eliminating manual platform hopping and improving data quality.

---

## 🎯 Project Overview
Searching for careers across fragmented platforms like LinkedIn, Indeed, and Google causes **fatigue and data fragmentation**. This manual process often leads to duplicate entries and exposure to "ghost job" listings from third-party aggregators that clutter search results.

## 🚀 Core Features
* **Orchestrated Search:** Queries multiple major boards simultaneously using a single, parameterized configuration block.
* **Data Hygiene:** Automatically removes listings from known low-quality aggregators and deduplicates results.
* **Operational Resiliency:** Implements random jitter and stealth logic to maintain long-term access and prevent rate limits.
* **Automated Rotation:** Includes a built-in retention policy to manage local data storage and ensure a clean workspace.

## 🛠 Technical Architecture
* **Language:** Python 3.12
* **Sourcing Engine:** `python-jobspy` (API-less multi-platform aggregation)
* **Data Processing:** `Pandas`
* **File Management:** `Pathlib` (Object-oriented filesystem paths)
* **Privacy:** Robust ignore rules to safeguard personal data and local environments.

## ⚙️ Configuration
The engine is decoupled from the search logic. To run your own search, update the `config.yaml` file with your specific parameters:

* **Boolean Strings:** Supports complex queries (e.g., `(Role A OR Role B) AND Industry`).
* **Platform Control:** Toggle between LinkedIn, Indeed, and Google Jobs.
* **Smart Filtering:** Add known low-quality boards to the `clutter_list` to scrub them from your results.

## 📦 Installation
1. Clone the repository.
2. Create a virtual environment: `python -m venv .venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the engine: `python lead_sourcing_engine.py`

## 📈 Business Impact
By automating the discovery phase of the search process, this engine reduces manual overhead by an estimated **80%**. This efficiency allows for a pivot away from data collection and toward high-value activities like application tailoring and strategic networking.
                                               
## ⚠️ Disclaimer & Ethics ⚠️

This tool is intended for personal career research and educational purposes. Because it relies on web scraping via python-jobspy, its functionality is subject to change based on updates to the host platforms' site structures. Users should adhere to the Terms of Service of the respective job boards and implement responsible scraping practices (e.g., using the built-in jitter and limiting request frequency).