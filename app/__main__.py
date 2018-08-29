from jobs.scrap import scrap_olx_iphone8
from jobs.upload import load_to_gbq
from jobs.query import get_avg_price_by_city, get_most_offers_by_city, get_most_least_expensive

if __name__ == "__main__":
    file_path = scrap_olx_iphone8()
    load_to_gbq(file_path)
    get_avg_price_by_city()
    get_most_offers_by_city()
    get_most_least_expensive()
