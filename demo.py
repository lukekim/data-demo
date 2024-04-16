import time
from time import sleep
from spicepy import Client
import threading

###########################
#   Spice AI Platform     #
###########################

# use API key from Spice.ai app to instantiate a client

# client = Client('3232|f0121ee340b04a02b912e4e08339133e')

# startTime = time.time()
# data = client.query('SELECT * FROM eth.recent_traces trace JOIN eth.recent_transactions trans ON trace.transaction_hash = trans.hash ORDER BY trans.block_number DESC;')
# pd = data.read_chunk()
# endTime = time.time()

# print("Query Time: " + str(endTime - startTime) + " seconds\n")

# exit()

########################################
#   DO NOT COMMENT OUT THE LINE BELOW  #
########################################
client = Client('3232|f0121ee340b04a02b912e4e08339133e', 'grpc://127.0.0.1:50051')

###########################
#   Spice AI Datasource   #
###########################

while True:
    startTime = time.time()
    data = client.query('SELECT trace.block_number FROM eth_recent_traces trace JOIN eth_recent_transactions trans ON trace.transaction_hash = trans.hash ORDER BY trans.block_number DESC;')
    pd = data.read_pandas()
    endTime = time.time()

    print(pd.head(5))
 
    print("Query Time: " + str(endTime - startTime) + " seconds\n")

    sleep(1)

###########################
#    Dremio Datasource    #
###########################

while True:
    startTime = time.time()
    data = client.query('SELECT * FROM taxi_trips ORDER BY pickup_datetime DESC LIMIT 100')
    endTime = time.time()
    pd = data.read_pandas()

    print(pd.to_string() + "\n")
    print("Query Time: " + str(endTime - startTime) + " seconds\n")

    startTime = time.time()
    data = client.query('SELECT count(*) FROM taxi_trips')
    endTime = time.time()
    pd = data.read_pandas()

    print(pd.to_string() + "\n")
    print("Query Time: " + str(endTime - startTime) + " seconds\n")

###########################
# Spice/Dremio Datasource #
###########################

# while True:
#     startTime = time.time()
#     data = client.query("""
#         SELECT DISTINCT
#             eth_recent_blocks.number as block_number, 
#             taxi_trips.trip_distance_mi
#         FROM eth_recent_blocks 
#         LEFT JOIN taxi_trips 
#         ON eth_recent_blocks.number%100 = taxi_trips.trip_distance_mi*10
#         ORDER BY eth_recent_blocks.number DESC                
#         LIMIT 10
#         """)
#     endTime = time.time()
#     pd = data.read_pandas()

#     print(pd.to_string() + "\n")
#     print("Query Time: " + str(endTime - startTime) + " seconds\n")

#     sleep(5)