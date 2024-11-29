from src.wallet import Wallet
from src.transactions import Transaction
from src.blockchain import Blockchain
from src.block import Block
from datetime import datetime

def main():
    # Initialize blockchain with empty chain and mempool
    blockchain = Blockchain(
        chain=[],
        difficulty=2,
        mempool=[],
        block_reward=50.0
    )

    # Create the genesis block
    blockchain.create_genesis_block()

    # Initialize wallets for Alice and Bob
    alice_wallet = Wallet(blockchain)
    bob_wallet = Wallet(blockchain)

    print(f"Alice's Address: {alice_wallet.address}")
    print(f"Bob's Address: {bob_wallet.address}")

    # Check initial balances
    print(f"Alice's Balance: {alice_wallet.get_balance()} BTC")
    print(f"Bob's Balance: {bob_wallet.get_balance()} BTC")

    # Mine pending transactions (should include only the genesis block's transactions)
    blockchain.mine_pending_transactions(miner_address=alice_wallet.address)

    # Check balances after mining
    print(f"Alice's Balance after mining: {alice_wallet.get_balance()} BTC")
    print(f"Bob's Balance after mining: {bob_wallet.get_balance()} BTC")

    # Create a transaction from Alice to Bob
    transaction = Transaction(
        sender_address=alice_wallet.get_pem_public_key(),
        recipient_address=bob_wallet.get_pem_public_key(),
        amount=10.0
    )

    # Alice signs the transaction
    alice_wallet.sign_transaction(transaction)

    # Add the transaction to the blockchain's mempool
    blockchain.add_transaction(transaction)

    # Check balances before mining
    print(f"Alice's Balance before mining: {alice_wallet.get_balance()} BTC")
    print(f"Bob's Balance before mining: {bob_wallet.get_balance()} BTC")

    # Mine pending transactions
    blockchain.mine_pending_transactions(miner_address=alice_wallet.address)

    # Check balances after mining
    print(f"Alice's Balance after mining: {alice_wallet.get_balance()} BTC")
    print(f"Bob's Balance after mining: {bob_wallet.get_balance()} BTC")

if __name__ == "__main__":
    main()
