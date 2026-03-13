import sys

def main(job_params):
    env, target, table, operation, timestamp, starttime, endtime, dry_run = job_params

    if env == "dev":
        import dev.upsert as upsert
    elif env == "prod":
        import prod.upsert as upsert
    else:
        raise ValueError("Invalid environment")

    if operation == "upsert":
        upsert.run(table, timestamp, starttime, endtime, dry_run)
    else:
        raise ValueError("Unsupported operation")

if __name__ == "__main__":
    # Example: ["dev","datamart","credit_card_data_mart","upsert","2026-03-05T00:00:00","2026-03-05T00:00:00","2026-03-05T01:00:00",False]
    job_params = sys.argv[1:]
    main(job_params)