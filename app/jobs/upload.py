from google.cloud import bigquery


def load_to_gbq(file_path):
    print('--- Starting file loading to cloud ---\n')

    client = bigquery.Client()
    dataset_id = 'web_scraper'
    table_id = 'product'

    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1
    job_config.write_disposition = 'WRITE_TRUNCATE'
    job_config.schema = [
        bigquery.SchemaField('id', 'INTEGER', mode='REQUIRED'),
        bigquery.SchemaField('date', 'DATE'),
        bigquery.SchemaField('company', 'STRING'),
        bigquery.SchemaField('state', 'STRING'),
        bigquery.SchemaField('city', 'STRING'),
        bigquery.SchemaField('title', 'STRING'),
        bigquery.SchemaField('price', 'INTEGER'),
    ]

    with open(file_path, 'rb') as source_file:
        job = client.load_table_from_file(
            source_file,
            table_ref,
            location='US',  # Must match the destination dataset location.
            job_config=job_config)  # API request

    job.result()  # Waits for table load to complete.

    print('Loaded {} rows into {}:{}.\n'.format(
        job.output_rows, dataset_id, table_id))

    print('--- Finished file loading to cloud ---\n')
