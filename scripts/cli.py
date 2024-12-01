# scripts/cli.py

import argparse
from src.wallet import Wallet
from src.transactions import Transaction
from src.blockchain import Blockchain
from src.block import Block
from datetime import datetime
import json
import sys
import os

def load_wallets(blockchain: Blockchain) -> dict:
    """
    Loads all wallets from the 'wallets' directory.

    Args:
        blockchain (Blockchain): The blockchain instance to associate with wallets.

    Returns:
        dict: A dictionary of wallets with labels as keys.
    """
    wallets = {}
    wallets_dir = "wallets"
    if os.path.exists(wallets_dir):
        for filename in os.listdir(wallets_dir):
            if filename.endswith(".json"):
                label = filename[:-5]  # Remove '.json' extension
                wallet = Wallet(blockchain, label)
                wallets[label] = wallet
    return wallets

def main():
    # Load existing blockchain or create a new one
    blockchain = Blockchain.load_from_file()

    # Load existing wallets
    wallets = load_wallets(blockchain)

    parser = argparse.ArgumentParser(description="btc_light Blockchain CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Create Wallet
    parser_create_wallet = subparsers.add_parser('create_wallet', help='Create a new wallet')
    parser_create_wallet.add_argument('label', type=str, help='Label for the wallet')

    # Check Balance
    parser_check_balance = subparsers.add_parser('check_balance', help='Check wallet balance')
    parser_check_balance.add_argument('label', type=str, help='Label of the wallet')

    # Send Transaction
    parser_send_tx = subparsers.add_parser('send_transaction', help='Send a transaction')
    parser_send_tx.add_argument('from_label', type=str, help='Sender wallet label')
    parser_send_tx.add_argument('to_label', type=str, help='Recipient wallet label')
    parser_send_tx.add_argument('amount', type=float, help='Amount to send')

    # Mine Block
    parser_mine = subparsers.add_parser('mine_block', help='Mine pending transactions')
    parser_mine.add_argument('miner_label', type=str, help='Wallet label of the miner')

    # View Chain
    parser_view = subparsers.add_parser('view_chain', help='View the entire blockchain')
    parser_view.add_argument('--num_blocks', type=int, default=5, help='Number of blocks to view')

    # Validate Chain
    parser_validate = subparsers.add_parser('is_valid', help='Validate the blockchain')

    args = parser.parse_args()

    if args.command == 'create_wallet':
        label = args.label
        if label in wallets:
            print(f"Wallet with label '{label}' already exists.")
            sys.exit(1)
        wallet = Wallet(blockchain, label)
        wallets[label] = wallet
        print(f"Wallet '{label}' created with address: {wallet.address}")

    elif args.command == 'check_balance':
        label = args.label
        if label not in wallets:
            print(f"Wallet with label '{label}' does not exist.")
            sys.exit(1)
        wallet = wallets[label]
        balance = wallet.get_balance()
        print(f"Wallet '{label}' Balance: {balance} BTC")

    elif args.command == 'send_transaction':
        from_label = args.from_label
        to_label = args.to_label
        amount = args.amount

        if from_label not in wallets:
            print(f"Sender wallet '{from_label}' does not exist.")
            sys.exit(1)
        if to_label not in wallets:
            print(f"Recipient wallet '{to_label}' does not exist.")
            sys.exit(1)
        sender_wallet = wallets[from_label]
        recipient_wallet = wallets[to_label]

        # Check if sender has enough balance
        sender_balance = sender_wallet.get_balance()
        if sender_balance < amount:
            print(f"Transaction rejected: Sender '{from_label}' has insufficient balance ({sender_balance} BTC).")
            sys.exit(1)

        # Create and sign the transaction
        tx = Transaction(
            sender_address=sender_wallet.get_pem_public_key(),
            recipient_address=recipient_wallet.get_pem_public_key(),
            amount=amount
        )
        sender_wallet.sign_transaction(tx)

        # Add transaction to blockchain
        blockchain.add_transaction(tx)

        # Save the updated blockchain
        blockchain.save_to_file()

    elif args.command == 'mine_block':
        miner_label = args.miner_label
        if miner_label not in wallets:
            print(f"Miner wallet '{miner_label}' does not exist.")
            sys.exit(1)
        miner_wallet = wallets[miner_label]
        blockchain.mine_pending_transactions(miner_address=miner_wallet.address)

        # Save the updated blockchain
        blockchain.save_to_file()

    elif args.command == 'view_chain':
        num_blocks = args.num_blocks
        chain_length = len(blockchain.chain)
        start_index = max(0, chain_length - num_blocks)
        blocks_to_view = blockchain.chain[start_index:]

        def render_block(block):
            transactions = "\n".join(
                f"    - {tx.to_dict()}" for tx in block.transactions
            )
            transactions = transactions if transactions else "    No Transactions"
            return (
                f" ________________________\n"
                f"| Block {str(block.index)}                |\n"
                f"|________________________|\n"
                f"|      Timestamp:        |\n"
                f"| {block.timestamp[:22]} |\n"
                f"|------------------------|\n"
                f"| Prev. Hash: {block.prev_hash[:8]}          |\n"
                f"|------------------------|\n"
                f"|         Hash:          |\n"
                f"| {block.hash[:8]:<22} |\n"
                f"|------------------------|\n"
                f"|  Nonce: {str(block.nonce)}           |\n"
                f"|------------------------|\n"
                f"|     Transactions:      |\n"
                f"|{transactions}     |\n"        
                f"|________________________|"
            )

        for i, block in enumerate(blocks_to_view):
            print(render_block(block))
            if i < len(blocks_to_view) - 1:
                print("           |              ")
                print("           v              ")

    elif args.command == 'is_valid':
        is_valid = blockchain.is_chain_valid()
        print(f"Blockchain valid: {is_valid}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
