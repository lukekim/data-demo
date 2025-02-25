# Spice.ai Data Demo

The data demo shows getting started with Spice in 5 mins for federated queries, local materialization, and acceleration.

## Machine Setup

```bash
# Clone this repository
git clone git@github.com:lukekim/data-demo.git
cd data-demo

# Setup Python Virtual Environment
python -m venv venv

# Install the SpicePy Python package
pip install git+https://github.com/spiceai/spicepy@v1.0.1
```

Edit `demo.py` and set the API key on line 6.

E.g.

```python
SPICEAI_API_KEY = '3232|f42bb127dceb48cab83437264897b06a'
```

## Data demo

### Step 1. Show cloud data warehouse (CWD) performance in the Spice.ai Playground

Navigate to the Spice.ai Playground. E.g. [spice.ai/lukekim/demo/playground](https://spice.ai/lukekim/demo/playground).

Execute the query:

```sql
SELECT * from eth.recent_blocks LIMIT 10;
```

Note that it's very fast... subsecond.

Execute a more compute intensive query. A join across two large datasets:

```sql
SELECT *
FROM eth.recent_traces trace
JOIN eth.recent_transactions trans ON trace.transaction_hash = trans.hash
ORDER BY trans.block_number DESC
```

Note that while still fast it takes 5-7 seconds to complete because it's fetching ~130K rows over HTTP.

### Step 2. Show the same query using the Spice Python SDK to simulate app or Notebook usage

Install the Spice CLI:

```bash
curl https://install.spiceai.org | /bin/bash
```

Open `demo.py` in VS Code or another editor.

Show that it's the same query as above, but this time we'll run it from the Python script simulating an app or Notebook.

```bash
python demo.py
```

Note that it takes about 2-3 seconds to complete. An improvement over the Playground because it's using Apache Arrow Flight not HTTP/JSON.

### Step 2. Show getting started with Spice OSS and performance of local queries

```bash
# Initialize the Spice app and show the generated spicepod.yaml
spice init

# Set the name to "smart"

# Log in to the Spice.ai platform
spice login

# Start the Spice runtime
spice run
```

Note, the runtime starts HTTP, Arrow Flight, and OTEL endpoints.

Open another terminal window so the runtime can continue to run.

```bash
# Add the lukekim/demo spicepod
spice add lukekim/demo
```

Note the four loaded datasets in the runtime logs.

Open `/spicepods/lukekim/demo/spicepod.yaml` and show the dataset definitions.

```bash
# Start the Spice SQL REPL
spice sql

# Execute the show tables query
sql> show tables;
+---------------+--------------------+--------------------------+------------+
| table_catalog | table_schema       | table_name               | table_type |
+---------------+--------------------+--------------------------+------------+
| datafusion    | public             | eth_recent_transactions  | BASE TABLE |
| datafusion    | public             | eth_recent_traces        | BASE TABLE |
| datafusion    | public             | eth_recent_blocks_duckdb | BASE TABLE |
| datafusion    | public             | eth_recent_blocks        | BASE TABLE |
| datafusion    | information_schema | tables                   | VIEW       |
| datafusion    | information_schema | views                    | VIEW       |
| datafusion    | information_schema | columns                  | VIEW       |
| datafusion    | information_schema | df_settings              | VIEW       |
+---------------+--------------------+--------------------------+------------+

Query took: 0.006861292 seconds
```

Note the four datasets from the Spicepod are now loaded.

```bash
# Execute a query on the recent blocks table
sql> select * from eth_recent_blocks;

# Exit the REPL
sql> exit
```

Open `demo.py` again, comment out the first code block. Note line 28 `client = Client(SPICEAI_API_KEY, 'grpc://127.0.0.1:50051')` configuring the SDK to use the local Spice runtime.
