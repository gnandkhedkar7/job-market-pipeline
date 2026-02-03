import sys
from datetime import datetime

from src.scripts.parse_and_store_jobs import main as parse_jobs
from src.cleaning.clean_and_store_jobs import main as clean_jobs
from src.cleaning.extract_and_store_skills import main as extract_skills
from src.analytics.build_daily_skill_counts import main as update_daily_counts

def run_step(name, fn):
    print(f"\n Starting step: {name}")
    start = datetime.utcnow()
    
    try:
        fn()
    except Exception as e:
        print(f"Step failed: {name}")
        print(e)
        sys.exit(1)
        
    elapsed = (datetime.utcnow() - start).seconds
    print(f"Finished {name} in {elapsed}s")
    
def main():
    run_step("Parse jobs", parse_jobs)
    run_step("Clean jobs", clean_jobs)
    run_step("Extract skills", extract_skills)
    run_step("Update daily skill counts", update_daily_counts)
    
    print("\n Pipeline completed successfully")
    
if __name__ == "__main__":
    main()