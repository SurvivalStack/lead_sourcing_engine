from jobspy import scrape_jobs
import pandas as pd
from datetime import datetime

# High-signal search query for support leadership
search_term = '("Customer Support" OR "Technical Support" OR "Customer Success") AND (Manager OR "Senior Manager" OR Director OR "Head of" OR VP) AND ("SaaS" OR "Cloud" OR "Software")'

print(f"[{datetime.now().strftime('%H:%M:%S')}] Querying Job Boards...")

try:
    # Aggregating leads from three major platforms
    jobs = scrape_jobs(
        site_name=["linkedin", "indeed", "zip_recruiter", "google"],
        search_term=query,
        location="Remote", 
        results_wanted=15,
        hours_old=72, 
        country_indeed='USA'
    )

    if not jobs.empty:
        # Standardizing output for your 'ats_jobboard_directory'
        output_file = f"leads_{datetime.now().strftime('%Y-%m-%d')}.csv"
        jobs.to_csv(output_file, index=False)
        
        print("-" * 30)
        print(f"SUCCESS: Found {len(jobs)} potential matches.")
        print(f"Data saved to: {output_file}")
        print("-" * 30)
        
        # Quick preview of the top 3
        print(jobs[['company', 'title', 'location']].head(3))
    else:
        print("Search completed: No new roles found matching your criteria in the last 72h.")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")