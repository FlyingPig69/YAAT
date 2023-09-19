# YAAT
Yet Another Airdrop Tool - Massive version. For airdropping tokens to large amount addresses on the Ergo Blockchain with minimum fees
If aidropping to thousands of records it supports splitting the drop into x number of parts. Each will be submitted sequentially once the previous has been confirmed by the blockchain

# Requirements
Requires Ergpy (by mgpai)
https://github.com/mgpai22/ergpy

# Usage

Create a CSV file containing your aidrop list and 4 columns and lace in same folder as YAAT.py.

See sample.csv


**Step 1**
1. Address - recipient address
2. Token_ID - Token ID of the token you want to send
3. Token_Amount - Amount of token
4. Erg_amount - amount of erg to send. For each address you are sending to this will be the input required. Min seems to be 0.00004

You can send different tokens to the same address as long as it's on a different row. 

**Step 2**

Open YAAT.py in your python editor of choice.

Edit config:

* input_file = 'aidrop.csv'                   name of your csv file. Place in same folder as this python script. Column order: (address, token_id, token_amount,erg_amount)

* node_url = "http://213.239.193.208:9053/"   Node

* wallet_mnemonic = "YOUR SEED PHRASE HERE"   Your wallet seed phrase

* batch_size = 1                              Number of transactions/outputs per batch. This will split your list file into x parts. Useful for LAARGE airdrops. 2000 seems to be the limit for 1 token (93kb, 96kb being limit).

* confirmations = 1                           Number of blocks to wait before processing next batch after previous batch was confirmed.

* miner_fee = 0.0012                          Miner fee, set higher for larger txs to ensure it's not stuck for a number of blocks....


**Step 3**

Run the script and wait....If you're airdropping thousands of records it can take a while.



