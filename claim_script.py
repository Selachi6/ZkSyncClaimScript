import json
import time
from web3 import Web3
from datetime import datetime



target_time = 1718606700
def wait_until_target_time(target_time):
    while True:
        current_time = int(time.time())
        time_left = target_time - current_time
        if time_left <= 0:
            break
        print(f"Time left until target time: {time_left} seconds")
        time.sleep(1)

# Connect to zkSync node
zksync_rpc_url = 'https://mainnet.era.zksync.io'  #CHANGE RPC HERE
web3 = Web3(Web3.HTTPProvider(zksync_rpc_url))

# Check if the connection is successful
if not web3.is_connected():
    raise Exception("Failed to connect to zkSync RPC")

# Distributor address on zkSync
contract_address = ''


# ABI of the contract, CHANGE IF NEEDED
abi = '''
[{"inputs":[{"internalType":"address","name":"_admin","type":"address"},{"internalType":"contract IMintableAndDelegatable","name":"_token","type":"address"},{"internalType":"bytes32","name":"_merkleRoot","type":"bytes32"},{"internalType":"uint256","name":"_maximumTotalClaimable","type":"uint256"},{"internalType":"uint256","name":"_windowStart","type":"uint256"},{"internalType":"uint256","name":"_windowEnd","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"currentNonce","type":"uint256"}],"name":"InvalidAccountNonce","type":"error"},{"inputs":[],"name":"InvalidShortString","type":"error"},{"inputs":[{"internalType":"string","name":"str","type":"string"}],"name":"StringTooLong","type":"error"},{"inputs":[],"name":"ZkMerkleDistributor__AlreadyClaimed","type":"error"},{"inputs":[],"name":"ZkMerkleDistributor__ClaimAmountExceedsMaximum","type":"error"},{"inputs":[],"name":"ZkMerkleDistributor__ClaimWindowNotOpen","type":"error"},{"inputs":[],"name":"ZkMerkleDistributor__ClaimWindowNotYetClosed","type":"error"},{"inputs":[],"name":"ZkMerkleDistributor__ExpiredSignature","type":"error"},{"inputs":[],"name":"ZkMerkleDistributor__InvalidProof","type":"error"},{"inputs":[],"name":"ZkMerkleDistributor__InvalidSignature","type":"error"},{"inputs":[],"name":"ZkMerkleDistributor__SweepAlreadyDone","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"ZkMerkleDistributor__Unauthorized","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"index","type":"uint256"},{"indexed":false,"internalType":"address","name":"account","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Claimed","type":"event"},{"anonymous":false,"inputs":[],"name":"EIP712DomainChanged","type":"event"},{"inputs":[],"name":"ADMIN","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAXIMUM_TOTAL_CLAIMABLE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MERKLE_ROOT","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"TOKEN","outputs":[{"internalType":"contract IMintableAndDelegatable","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"WINDOW_END","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"WINDOW_START","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ZK_CLAIM_AND_DELEGATE_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ZK_CLAIM_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_index","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"bytes32[]","name":"_merkleProof","type":"bytes32[]"}],"name":"claim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_index","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"bytes32[]","name":"_merkleProof","type":"bytes32[]"},{"components":[{"internalType":"address","name":"delegatee","type":"address"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"bytes","name":"signature","type":"bytes"}],"internalType":"struct ZkMerkleDistributor.DelegateInfo","name":"_delegateInfo","type":"tuple"}],"name":"claimAndDelegate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_index","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"bytes32[]","name":"_merkleProof","type":"bytes32[]"},{"components":[{"internalType":"address","name":"claimant","type":"address"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"bytes","name":"signature","type":"bytes"}],"internalType":"struct ZkMerkleDistributor.ClaimSignatureInfo","name":"_claimSignatureInfo","type":"tuple"},{"components":[{"internalType":"address","name":"delegatee","type":"address"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"bytes","name":"signature","type":"bytes"}],"internalType":"struct ZkMerkleDistributor.DelegateInfo","name":"_delegateInfo","type":"tuple"}],"name":"claimAndDelegateOnBehalf","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_index","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"bytes32[]","name":"_merkleProof","type":"bytes32[]"},{"components":[{"internalType":"address","name":"claimant","type":"address"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"bytes","name":"signature","type":"bytes"}],"internalType":"struct ZkMerkleDistributor.ClaimSignatureInfo","name":"_claimSignatureInfo","type":"tuple"}],"name":"claimOnBehalf","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"eip712Domain","outputs":[{"internalType":"bytes1","name":"fields","type":"bytes1"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"version","type":"string"},{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"address","name":"verifyingContract","type":"address"},{"internalType":"bytes32","name":"salt","type":"bytes32"},{"internalType":"uint256[]","name":"extensions","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"invalidateNonce","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_index","type":"uint256"}],"name":"isClaimed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_unclaimedReceiver","type":"address"}],"name":"sweepUnclaimed","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"totalClaimed","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]
'''


contract = web3.eth.contract(address=contract_address, abi=json.loads(abi))

# Function to claim tokens
def claim_tokens(wallet_address, private_key, index, amount, merkle_proof):
    nonce = web3.eth.get_transaction_count(wallet_address)
    txn = contract.functions.claim(index, amount, merkle_proof).build_transaction({
        'chainId': 324, 
        'gas': 150000, #CHANGE GAS HERE
        'gasPrice': web3.to_wei('5', 'gwei'), #CHANGE GAS PRICE HERE
        'nonce': nonce,
    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return web3.to_hex(tx_hash)




# FILL YOUR WALLET DETAILS HERE
wallets = [
    {
        "wallet_address": "wallet_address1",
        "private_key": 'private_key1',
        "index": 000000,
        "amount": 000000,
        "merkle_proof": []
    },

    {
        "wallet_address": "wallet_address2",
        "private_key": "private_key2",
        "index": 000000,
        "amount": 000000,
        "merkle_proof": []
    }
]

wait_until_target_time(target_time)

for wallet in wallets:
    try:
        tx_hash = claim_tokens(
            wallet['wallet_address'],
            wallet['private_key'],
            wallet['index'],
            wallet['amount'],
            wallet['merkle_proof']
        )
        print(f"Transaction hash for {wallet['wallet_address']}: {tx_hash}")
    except Exception as e:
        print(f"Error claiming tokens for {wallet['wallet_address']}: {e}")