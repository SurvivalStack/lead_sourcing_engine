import random
import time
import pandas as pd
from pathlib import Path
from datetime import datetime
from jobspy import scrape_jobs

# ==========================================
# CONFIGURATION - EDIT THESE SETTINGS
# ==========================================
SEARCH_TERM = query = '("Customer Support" OR "Technical Support") AND (Manager OR "Senior Manager" OR Director OR "Head of" OR VP) AND ("SaaS" OR "Cloud" OR "Software")'
LOCATION = "USA"
SITES = ["linkedin", "indeed", "google"]
RESULTS_WANTED = 20
IS_REMOTE = True

# Retention Policy
MAX_FILES = 14  # Floor: Minimum number of files to keep
MAX_DAYS = 30   # Window: Number of days to keep files

# List of companies/aggregators to exclude from results
CLUTTER_LIST = ["Swooped", "Lensa", "Talentify", "Jobright", "MyJobHelper", "Jooble"]
# ==========================================

def rotate_leads(max_files, max_days):
    """Prunes old lead files based on count and age constraints."""
    path = Path(".")
    files = sorted(list(path.glob("jobleads_*.csv")), key=lambda x: x.name, reverse=True)
    
    if not files:
        return

    current_time = datetime.now()
    for index, file_path in enumerate(files):
        try:
            parts = file_path.stem.split('_')
            file_date = datetime.strptime(f"{parts}_{parts}", "%Y%m%d_%H%M")
            age = (current_time - file_date).days
            
            # Keep if within the 'X' newest files OR within the day window
            if index < max_files or age <= max_days:
                continue
            
            file_path.unlink()
            print(f"  - Pruned stale file: {file_path.name}")
        except Exception:
            continue

def run_sourcing_engine():
    """Executes the job search with anti-scraping measures and filtering."""
    all_leads = []
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Initializing Lead Sourcing...")

    for site in SITES:
        try:
            print(f"Searching {site}...")
            results = scrape_jobs(
                site_name=[site],
                search_term=SEARCH_TERM,
                location=LOCATION,
                results_wanted=RESULTS_WANTED, 
                hours_old=72,
                country_indeed="usa",
                linkedin_fetch_description=True,
                is_remote=IS_REMOTE
            )
            
            if not results.empty:
                all_leads.append(results)
            
            # STEALTH: Random jitter between 21 and 42 seconds
            time.sleep(random.uniform(21, 42))
                
        except Exception as e:
            print(f"  - Error querying {site}: {e}")

    if all_leads:
        final_df = pd.concat(all_leads)
        
        # Clean and Filter
        final_df = final_df[~final_df["company"].isin(CLUTTER_LIST)]
        final_df = final_df.drop_duplicates(subset=["job_url"])
        
        # Output: jobleads_YYYYMMDD_HHMM.csv
        filename = datetime.now().strftime("leads_%Y%m%d_%H%M.csv")
        final_df.to_csv(filename, index=False)
        print(f"SUCCESS: {len(final_df)} unique leads saved to {filename}")
        
        rotate_leads(MAX_FILES, MAX_DAYS)
    else:
        print("\nNo new leads found in this session.")

if __name__ == "__main__":
    run_sourcing_engine()