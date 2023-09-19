#  YAAT - Massive Version
#  Yet Another Aidrop Tool
#  -----
# Use YAAT to distribute tokens to a MASSIVE number of addresses from a csv file.
# It overcomes the TX limit (approx 2000 outputs) by splitting the list into chunks (configurable) and sending sequentially. 
# 
# ------
#  by Flying_Pig69
#  Open Source, free to use and modify by anyone! You don't even need to give credit (although it would be nice :p)

import csv
import time
import requests
from ergpy import appkit
from ergpy import helper_functions

#config items
input_file = 'aidrop.csv' # name of your csv file. Place in same folder as this python script. Column order: (address,	token_id, token_amount,erg_amount).
node_url = "http://213.239.193.208:9053/" # Node
wallet_mnemonic = "YOUR SEED PHRASE HERE" # your wallet seed phrase
batch_size = 2000 # number of transactions/outputs per batch. This will split your list file into x parts. Useful for LAARGE airdrops. 2000 seems to be the limit for 1 token (93kb, 96kb being limit).
confirmations = 1 # no of blocks to wait before processing next batch after previous batch was confirmed. If left 0 it will send the next transactions immediately when the previous has been confirmed. I reccommend leaving at 1...just in case.
miner_fee = 0.0012 # miner fee, set higher for larger txs to ensure it's not stuck for a number of blocks....


# ----------------------no need to modify anything below this line -------------
# Initialize objects
ergo = appkit.ErgoAppKit(node_url)
addresses_full = []
token_id_full = []
token_amount_full = []
erg_amount_full = []
no_submitted = 0
no_unconfirmed = 0
wallet_address = helper_functions.get_wallet_address(ergo=ergo, amount=1, wallet_mnemonic=wallet_mnemonic)[0]

# get number of unconfirmed transactions for sender address.
def unconfirmed():
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    get_ergtree=(node_url+"script/addressToTree/"+wallet_address)

    # get ergotree from address
    response = requests.get(get_ergtree)
    data = response.json()
    ergotree = data.get('tree')
    ergotree = ('"' + ergotree + '"')

    #get number of unconfirmed transactions for ergotree.
    get_unconfirmed = (node_url+"transactions/unconfirmed/byErgoTree?limit=10&offset=0")
    response = requests.post(get_unconfirmed, data=ergotree , headers=headers)
    response_json = response.json()
    no_unconfirmed = len(response_json)
    return no_unconfirmed

#split lists
def split_list(input_list, batch_size):
    for i in range(0, len(input_list), batch_size):
        yield input_list[i:i + batch_size]

#get current block height
def get_height():
    response = requests.get(node_url+"info")
    data = response.json()
    block_height = data.get('fullHeight')
    return block_height

# Open CSV file and split columns into separate lists
with open(input_file, 'r', newline='') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        if len(row) >= 4:
            addresses_full.append(row[0])
            token_id_full.append(row[1])
            token_amount_full.append(row[2])
            erg_amount_full.append(row[3])

#remove header rows
addresses_full.pop(0)
token_id_full.pop(0)
token_amount_full.pop(0)
erg_amount_full.pop(0)

#convert lists to expected format for sending transactions
token_amount_range = [[float(item)] for item in token_amount_full]
erg_amount_range = [float(item) for item in erg_amount_full]
token_id_range = [[item]for item in token_id_full]

#split list into batches
addresses = list(split_list(addresses_full, batch_size))
token_amounts = list(split_list(token_amount_range, batch_size))
token_ids = list(split_list(token_id_range, batch_size))
erg_amounts = list(split_list(erg_amount_range, batch_size))
no_parts=len(addresses)

print("")
print(len(addresses_full),"addresses split list into",no_parts,"parts with", len(addresses[0]),"outputs each.")

#main process
i = 0
for addresses in addresses:
    amount = erg_amounts[i]
    amount_tokens= token_amounts[i]
    receiver_address = addresses
    tokens=token_ids[i]
    print("----------------------------")
    print("Sending Tokens from:       ", wallet_address)
    print("Batch size (addressees):   ",len(receiver_address))
    print("Token:                     ",token_ids[0][0])
    print("Total ERG sent:            ",sum(amount))
    print("Miner Fee                  ",miner_fee)
    print("")

    #check if there are unconfirmed transactions. If there are wait until all are confirmed.
    no_unconfirmed = unconfirmed()
    while no_unconfirmed > 0:
        no_unconfirmed = unconfirmed()
        print("Sender address has",no_unconfirmed," transaction(s). Waiting for all to be confirmed before processing next batch.")
        if no_unconfirmed == None: #in case node can't be reached, try again until it get results.
            no_unconfirmed = 1
        time.sleep(30)

    print("Assembling transaction....for large amounts this can take several minutes")
    time.sleep(5)

    #submit transaction
    output_main = helper_functions.send_token(ergo=ergo, amount=amount, amount_tokens=amount_tokens,
                                      receiver_addresses=receiver_address, tokens=tokens, fee=miner_fee,
                                      wallet_mnemonic=wallet_mnemonic)

    #wait 15 seconds for transaction to propogate
    time.sleep(15)

    #if confirmations has been enabled, will wait x blocks until processing next batch.
    block_height = get_height()
    print("Submitted at height: ", block_height)
    no_submitted += 1
    next_height = block_height + confirmations

    while block_height < next_height:
        block_height = get_height()
        print("Current height:", block_height, ". Waiting for block", next_height,"before submitting next batch.", "Submitted", no_submitted, "of", no_parts, "parts")
        if block_height==None: #in case node can't be reached, try again until it get results.
            block_height = next_height-1
        time.sleep(10)

    print("----------------------------")
    i += 1

print("All parts submitted and confirmed.")
