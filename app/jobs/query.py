from google.cloud import bigquery


def get_avg_price_by_city():
    print('--> Qual o preço médio do produto por cidade?')

    client = bigquery.Client()

    query_job = client.query("""
                                SELECT p.city,
                                       CAST(AVG(p.price) AS INT64) AS average_price
                                FROM `data-team-test-777.web_scraper.product` p
                                GROUP BY p.city
                                ORDER BY average_price ASC
                            """)

    results = query_job.result()  # Waits for job to complete.

    for row in results:
        print("{} : R${}".format(row.city, row.average_price))


def get_most_offers_by_city():
    print('\n--> Qual a cidade que mais possui ofertas do produto?')
    client = bigquery.Client()

    query_job = client.query("""
                                SELECT p.city,
                                       COUNT(p.city) AS amount
                                FROM `data-team-test-777.web_scraper.product` p
                                GROUP BY p.city
                                ORDER BY amount DESC
                            """)

    results = query_job.result()  # Waits for job to complete.

    for row in results:
        print("{} : {} ofertas".format(row.city, row.amount))


def get_most_least_expensive():
    print('\n--> Liste os 5 mais baratos e o mais caro.')
    client = bigquery.Client()

    query_job = client.query("""
                                  (SELECT 'least expensive products' AS type,
                                          p.price,
                                          p.title,
                                          p.city,
                                          p.state
                                   FROM web_scraper.product p
                                   ORDER BY p.price ASC LIMIT 5)
                                UNION ALL
                                  (SELECT 'most expensive product' AS type,
                                          p.price,
                                          p.title,
                                          p.city,
                                          p.state
                                   FROM web_scraper.product p
                                   ORDER BY p.price DESC LIMIT 1)
                            """)

    results = query_job.result()  # Waits for job to complete.

    for row in results:
        print("{} : R${}, {}, {}, {}".format(row.type, row.price, row.title, row.city, row.state.upper()))

def run_all_queries():
    print('--- Respondendo as perguntas ---\n ')
    get_avg_price_by_city()
    get_most_offers_by_city()
    get_most_least_expensive()


# def get_avg_price_most_offers_by_city():
#     print('--- Qual o preço médio do produto por cidade? Qual a cidade que mais possui ofertas do produto? ---\n')
#
#     client = bigquery.Client()
#
#     query_job = client.query("""
#                                 SELECT p.city,
#                                        CAST(AVG(p.price) AS INT64) AS average_price,
#                                        count(p.city) AS amount
#                                 FROM `data-team-test-777.web_scraper.product` p
#                                 GROUP BY p.city
#                                 ORDER BY amount DESC
#                             """)
#
#     results = query_job.result()  # Waits for job to complete.
#
#     for row in results:
#         print("{} : R${}, {} ofertas".format(row.city, row.average_price, row.amount))
