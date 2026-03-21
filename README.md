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
* **Language:** Python 3.12+
* **Data Processing:** `Pandas`
* **File Management:** `Pathlib` (Object-oriented filesystem paths)
* **Privacy:** Robust ignore rules to safeguard personal data and local environments.

## 📈 Business Impact
By automating the discovery phase of the search process, this engine reduces manual overhead by an estimated **80%**. This efficiency allows for a pivot away from data collection and toward high-value activities like application tailoring and strategic networking.