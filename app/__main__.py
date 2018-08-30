from jobs.scrap import scrap_olx_iphone8
from jobs.upload import load_to_gbq
from jobs.query import run_all_queries
import sys


def main(**kwargs):
    step = 'all'

    for k, v in kwargs.items():
        if k == 'step':
            step = v

    if step == 'scrap' or step == 'all':
        file_path = scrap_olx_iphone8()
        load_to_gbq(file_path)

    if step == 'query' or step == 'all':
        run_all_queries()


if __name__ == '__main__':
    main(**dict(arg.replace('-', '').split('=') for arg in sys.argv[1:]))  # kwargs
