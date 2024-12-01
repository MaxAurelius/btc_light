# src/blockchain.py

import json
from typing import List, Dict
from .transactions import Transaction
from .block import Block
from datetime import datetime, timezone
import os

class Blockchain:
    """
    Manages the entire blockchain, including block addition, validation, and transaction handling.

    Attributes:
        chain (List[Block]): The list of all blocks in the blockchain.
        difficulty (int): The difficulty level for mining new blocks.
        mempool (List[Transaction]): A pool of pending transactions awaiting inclusion in a block.
        block_reward (float): The reward given to miners for successfully mining a block.
    """

    def __init__(
        self,
        chain: List[Block],
        difficulty: int,
        mempool: List[Transaction],
        block_reward: float,
    ) -> None:
        """
        Initializes the blockchain.

        Args:
            chain (List[Block]): The initial list of blocks in the blockchain.
            difficulty (int): The difficulty level for mining new blocks.
            mempool (List[Transaction]): The initial pool of pending transactions.
            block_reward (float): The reward given to miners for successfully mining a block.
        """
        self.chain: List[Block] = chain
        self.difficulty: int = difficulty
        self.mempool: List[Transaction] = mempool
        self.block_reward: float = block_reward

    def create_genesis_block(self) -> Block:
        """
        Creates the genesis (first) block in the blockchain.

        Returns:
            Block: The genesis block.
        """
        genesis_block = Block(
            index=0,
            transactions=[],
            timestamp=datetime.now(timezone.utc).isoformat(),
            prev_hash='0'
        )
        genesis_block.hash = genesis_block.calculate_hash()
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        return genesis_block

    def get_latest_block(self) -> Block:
        """
        Retrieves the latest block in the blockchain.

        Returns:
            Block: The most recent block.
        """
        return self.chain[-1]

    def add_block(self, new_block: Block) -> None:
        """
        Adds a new block to the blockchain after validating it.

        Args:
            new_block (Block): The block to be added.
        """
        new_block.prev_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self) -> bool:
        """
        Validates the integrity of the entire blockchain.

        Returns:
            bool: True if the blockchain is valid, False otherwise.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i-1]

            # Recalculate hash of the current block and compare
            if current_block.hash != current_block.calculate_hash():
                print(f"Invalid hash at block {current_block.index}")
                return False

            # Recalculate hash of the previous block and compare
            if prev_block.hash != prev_block.calculate_hash():
                print(f"Invalid hash at block {prev_block.index}")
                return False

            # Check if hash meets difficulty criteria
            if not current_block.hash.startswith('0' * self.difficulty):
                print(f"Block {current_block.index} has not been mined properly.")
                return False

        return True

    def add_transaction(self, transaction: Transaction) -> None:
        """
        Adds a new transaction to the mempool after verification.

        Args:
            transaction (Transaction): The transaction to be added.
        """
        sender_address = transaction.sender_address

        if sender_address == "Network":
            # Reward transactions don't require signature verification
            self.mempool.append(transaction)
            print("Reward transaction added to mempool.")
            return

        if not transaction.verify_signature():
            print("Invalid transaction signature. Transaction rejected.")
            return

        sender_balance = self.get_balance(sender_address)
        if sender_balance < transaction.amount:
            print(f"Sender '{sender_address}' has insufficient balance ({sender_balance} BTC). Transaction rejected.")
            return

        self.mempool.append(transaction)
        print("Transaction added to mempool.")

    def mine_pending_transactions(self, miner_address: str) -> None:
        """
        Mines all pending transactions, adds them to a new block, and rewards the miner.

        Args:
            miner_address (str): The address of the miner to receive the block reward.
        """

        # Create a reward transaction and add it to the mempool
        reward_tx = Transaction(
            sender_address="Network",
            recipient_address=miner_address,
            amount=self.block_reward
        )
        self.add_transaction(reward_tx)

        if not self.mempool:
            print("No transactions to mine.")
            return

        # Create a new block with all transactions in the mempool
        new_block = Block(
            index=len(self.chain),
            transactions=self.mempool.copy(),
            timestamp=datetime.now(timezone.utc).isoformat(),
            prev_hash=self.get_latest_block().hash
        )

        # Mine the new block
        new_block.mine_block(self.difficulty)

        # Add the mined block to the blockchain
        self.chain.append(new_block)
        print(f"Block {new_block.index} has been added to the blockchain.")

        # Clear the mempool after mining
        self.mempool.clear()

    def get_balance(self, address: str) -> float:
        """
        Calculates the balance of a given wallet address by aggregating transactions.

        Args:
            address (str): The wallet address to check the balance for.

        Returns:
            float: The calculated balance.
        """
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.recipient_address == address:
                    balance += tx.amount
                if tx.sender_address == address:
                    balance -= tx.amount
        return balance

    def to_dict(self) -> Dict:
        """
        Serializes the entire blockchain to a dictionary.

        Returns:
            Dict: The serialized blockchain.
        """
        return {
            'chain': [
                {
                    'index': block.index,
                    'transactions': [tx.to_dict() for tx in block.transactions],
                    'timestamp': block.timestamp,
                    'prev_hash': block.prev_hash,
                    'nonce': block.nonce,
                    'hash': block.hash
                }
                for block in self.chain
            ],
            'difficulty': self.difficulty,
            'mempool': [
                {
                    'sender_address': tx.sender_address,
                    'recipient_address': tx.recipient_address,
                    'amount': tx.amount,
                    'signature': tx.signature.hex() if tx.signature else None
                }
                for tx in self.mempool
            ],
            'block_reward': self.block_reward
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Blockchain':
        """
        Deserializes a dictionary to a Blockchain instance.

        Args:
            data (Dict): The serialized blockchain data.

        Returns:
            Blockchain: The deserialized blockchain instance.
        """
        chain = []
        for block_data in data['chain']:
            transactions = [
                Transaction(
                    sender_address=tx['sender_address'],
                    recipient_address=tx['recipient_address'],
                    amount=tx['amount'],
                    signature=bytes.fromhex(tx['signature']) if tx['signature'] else None
                )
                for tx in block_data['transactions']
            ]
            block = Block(
                index=block_data['index'],
                transactions=transactions,
                timestamp=block_data['timestamp'],
                prev_hash=block_data['prev_hash'],
                nonce=block_data['nonce'],
                hash=block_data['hash']
            )
            chain.append(block)

        mempool = [
            Transaction(
                sender_address=tx['sender_address'],
                recipient_address=tx['recipient_address'],
                amount=tx['amount'],
                signature=bytes.fromhex(tx['signature']) if tx['signature'] else None
            )
            for tx in data['mempool']
        ]

        return cls(
            chain=chain,
            difficulty=data['difficulty'],
            mempool=mempool,
            block_reward=data['block_reward']
        )

    def save_to_file(self, filename: str = 'blockchain.json') -> None:
        """
        Saves the blockchain state to a JSON file.

        Args:
            filename (str, optional): The filename to save the blockchain. Defaults to 'blockchain.json'.
        """
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)
        print(f"Blockchain saved to '{filename}'.")

    @classmethod
    def load_from_file(cls, filename: str = 'blockchain.json') -> 'Blockchain':
        """
        Loads the blockchain state from a JSON file.

        Args:
            filename (str, optional): The filename to load the blockchain from. Defaults to 'blockchain.json'.

        Returns:
            Blockchain: The loaded blockchain instance.
        """
        if not os.path.exists(filename):
            print("No existing blockchain found. Creating a new one with genesis block.")
            blockchain = cls(
                chain=[],
                difficulty=3,
                mempool=[],
                block_reward=50.0
            )
            blockchain.create_genesis_block()
            blockchain.save_to_file(filename)
            return blockchain

        with open(filename, 'r') as f:
            data = json.load(f)
            blockchain = cls.from_dict(data)
            print(f"Blockchain loaded from '{filename}'.")
            return blockchain
