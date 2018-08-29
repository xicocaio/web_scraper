from jobs.scrap import scrap_olx_iphone8
from jobs.upload import load_to_gbq
from jobs.query import run_all_queries

if __name__ == "__main__":
    file_path = scrap_olx_iphone8()
    load_to_gbq(file_path)
    run_all_queries()
