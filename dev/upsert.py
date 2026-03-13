from pyspark.sql import SparkSession
import dev.config as config   # dynamically swapped in main.py

spark = SparkSession.builder.getOrCreate()

def run(table, timestamp, starttime, endtime, dry_run=False):
    catalog = config.catalog
    schema = config.schema

    if table == config.credit_card_table:
        query = f"""
        MERGE INTO {catalog}.{schema}.{config.credit_card_table} AS target
        USING source_credit_card AS source
        ON target.customer_key = source.customer_key
        WHEN MATCHED AND source.gdp_processtime_stamp > target.load_time THEN
          UPDATE SET *
        WHEN NOT MATCHED THEN
          INSERT *;
        """
    elif table == config.email_table:
        query = f"""
        MERGE INTO {catalog}.{schema}.{config.email_table} AS target
        USING source_email AS source
        ON target.customer_key = source.customer_key
        WHEN MATCHED THEN
          UPDATE SET target.email_key = source.email_key,
                     target.timestamp = '{timestamp}',
                     target.load_time = '{endtime}';
        """
    elif table == config.name_table:
        query = f"""
        MERGE INTO {catalog}.{schema}.{config.name_table} AS target
        USING source_name AS source
        ON target.customer_key = source.customer_key
        WHEN MATCHED THEN
          UPDATE SET target.name_key = source.name_key,
                     target.timestamp = '{timestamp}',
                     target.load_time = '{endtime}';
        """
    else:
        raise ValueError(f"Unknown table: {table}")

    if dry_run:
        print("Dry run SQL:\n", query)
    else:
        spark.sql(query)
        print(f"Upsert completed for {table}")