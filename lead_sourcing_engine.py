import time
import random
import yaml
import pandas as pd
from pathlib import Path
from datetime import datetime
from jobspy import scrape_jobs

def load_config():
    """Loads configuration from the external YAML file."""
    try:
        with open("config.yaml", "r") as f:
            return yaml.safe_load(f)

    except FileNotFoundError:
        print("CRITICAL ERROR: config.yaml not found. Please create it.")
        exit(1)
        
config = load_config()
# ==========================================
# CONFIGURATION - config.yaml
# ==========================================
SEARCH_TERM = config['search']['term']
LOCATION = config['search']['location']
SITES = config['search']['sites']
RESULTS_WANTED = config['search']['results_wanted']
IS_REMOTE = config['search']['is_remote']

# Stealth and delay parameters, non-rhythmic delays between requests
JITTER_MIN = config['stealth']['jitter_min']
JITTER_MAX = config['stealth']['jitter_max']

# Retention Policy
MAX_FILES = config['retention']['max_files']
MAX_DAYS = config['retention']['max_days']

# List of companies/aggregators to exclude from results
CLUTTER_LIST = config['clutter_list']
# ==========================================

def rotate_leads(max_files, max_days):
    """Prunes old lead files based on count and age constraints."""
    path = Path(".")
    # FIXED: Look for "leads_" instead of "jobleads_"
    files = sorted(list(path.glob("leads_*.csv")), key=lambda x: x.name, reverse=True)
    
    if not files:
        return

    current_time = datetime.now()
    for index, file_path in enumerate(files):
        try:
            # Filename format: leads_YYYYMMDD_HHMM.csv
            parts = file_path.stem.split('_') 
            
            # FIXED: Index the list to get the actual date and time strings
            file_date = datetime.strptime(f"{parts[ 1 ]}_{parts[ 2 ]}", "%Y%m%d_%H%M")
            age = (current_time - file_date).days
            
            # Keep if within the 'X' newest files OR within the day window
            if index < max_files or age <= max_days:
                continue
            
            file_path.unlink()
            print(f"  - Pruned stale file: {file_path.name}")
        except Exception as e:
            # We skip errors here to ensure one bad filename doesn't kill the whole script
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
            wait_time = random.uniform(JITTER_MIN, JITTER_MAX)
            print(f"  - Stealth jitter: waiting {wait_time:.2f}s...")
            time.sleep(wait_time)
                
        except Exception as e:
            print(f"  - Error querying {site}: {e}")

    if all_leads:
        # 1. Sanitize sources to prevent the "FutureWarning"
        # We drop all-NA columns from each source before merging to avoid dtype confusion
        valid_leads = [df.dropna(axis=1, how='all') for df in all_leads if isinstance(df, pd.DataFrame) and not df.empty]
        
        # 2. Final check to ensure we have data left after cleaning
        valid_leads = [df for df in valid_leads if not df.empty]

        if valid_leads:
            # This is the line where the warning previously occurred
            final_df = pd.concat(valid_leads, ignore_index=True)
            
            # Clean and Filter
            if "company" in final_df.columns:
                final_df = final_df[~final_df["company"].isin(CLUTTER_LIST)]
            
            if "job_url" in final_df.columns:
                final_df = final_df.drop_duplicates(subset=["job_url"])
            
            # Output generation
            filename = datetime.now().strftime("leads_%Y%m%d_%H%M.csv")
            final_df.to_csv(filename, index=False)
            print(f"\nSUCCESS: {len(final_df)} unique leads saved to {filename}")
            
            rotate_leads(MAX_FILES, MAX_DAYS)
        else:
            print("\nNo valid data found after cleaning empty columns.")
    else:
        print("\nNo new leads found in this session.")

if __name__ == "__main__":
    run_sourcing_engine()