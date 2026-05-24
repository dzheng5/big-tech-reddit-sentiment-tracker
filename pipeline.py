from etl.ingest_block import IngestBlock
from etl.transform_block import TransformBlock
from etl.enrich_block import EnrichBlock
from etl.validate_block import ValidateBlock
from etl.load_block import LoadBlock

print("Starting pipeline...")

df = IngestBlock().run()
print(f"Ingested: {len(df)} rows")

df = TransformBlock().run(df)
print(f"Transformed: {len(df)} rows")

df = EnrichBlock().run(df)
print(f"Enriched: {len(df)} rows")

df = ValidateBlock().run(df)
print(f"Validated: {len(df)} rows")

LoadBlock().run(df)
print("Pipeline complete.")