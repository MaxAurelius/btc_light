from src.wallet import Wallet
from src.transactions import Transaction
from src.block import Block
from src.blockchain import Blockchain

from datetime import datetime, timezone

def main():
    # Initialize wallets for Alice and Bob
    alice_wallet = Wallet()
    bob_wallet = Wallet()

    print(f"Alice's Address: {alice_wallet.address}")
    print(f"Bob's Address: {bob_wallet.address}")

    # Create a transaction from Alice to Bob
    transaction = Transaction(
        sender_address=alice_wallet.get_pem_public_key(),
        recipient_address=bob_wallet.get_pem_public_key(),
        amount=10.0
    )

    # Alice signs the transaction
    alice_wallet.sign_transaction(transaction)

    # Verify the transaction's signature
    is_valid = transaction.verify_signature()
    print(f"Transaction valid: {is_valid}")

    if is_valid:
        print("Transaction has been successfully signed and verified.")
    else:
        print("Transaction signature is invalid.")

    # Create a block
    block = Block(
        index=1,
        transactions=[transaction],
        timestamp=datetime.now(timezone.utc).isoformat(),
        prev_hash='0'
    )

    difficulty = 5
    block.mine_block(difficulty)

    print(f"Block hash {block.hash}")

if __name__ == "__main__":
    main()
