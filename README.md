# YAAT - Massive Version
Yet Another Airdrop Tool - Massive version. 

For airdropping tokens to large number of addresses on the Ergo Blockchain with minimum fees. 

I used this script to distribute $lambo tokens to 65,000 addresses at the low low fee of 2.65 ERG (Transaction fees...there are no fees for using YAAT).
I was aiming for 170,000 but realized I only had around 4 ERG in my wallet. 
The max # of addresses is only limited by your RAM!

If airdropping to thousands of addresses you need to split the drop into several parts (in config). 
Each batch will be submitted sequentially once the previous has been confirmed by the blockchain. 

If you use this....feel free to add **9fLYPigGHXkTyyQvU9zzoT3RTAXJ4dfHjbkg6ik2fHKKxjprSrh** to your aidrop list :)

# Requirements
Requires Ergpy (by mgpai)
https://github.com/mgpai22/ergpy

# Usage

**Step 1**

CSV file format.
(See sample.csv)

1. Address - recipient address
2. Token_ID - Token ID of the token you want to send
3. Token_Amount - Amount of token
4. Erg_amount - amount of erg to send. Each address you are sending to needs a small amount of Erg. Minimum accepted seems to be 0.00004

You can send different tokens to the same address as long as it's on a separate row. (see sample.csv)

**Step 2**

Open YAAT.py in your python editor of choice.

Edit config section.

* **input_file**           
Name of your csv file. Place in same folder as this python script. Column order: (address, token_id, token_amount,erg_amount)

* **wallet_mnemonic**    
Your wallet seed phrase

* **batch_size**        
Number of transactions/outputs per batch. This will split your list file into x parts. Useful for LAARGE airdrops. 2000 seems to be the limit for 1 token (93kb, 96kb being limit). So if you're sending to 8000 addresses YAAT will create and send 4 transactions sequentially.

* **confirmations**      
Number of blocks to wait before processing next batch after previous batch was confirmed.
If set to 0 it will send the next transaction immediately once previous has been confirmed. I reccommend leaving at default 1. Just incase....


**Step 3**

Run the script and wait....If you're airdropping to thousands of addresses assembling each transaction takes a while....



