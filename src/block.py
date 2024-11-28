import json
from typing import List
from .transactions import Transaction
import hashlib


class Block:
    """
    Represents a single block within the blockchain.

    Attributes:
        index (int): The position of the block in the blockchain.
        transactions (List[Transaction]): A list of transactions included in the block.
        timestamp (float): The time at which the block was created.
        previous_hash (str): The hash of the previous block in the blockchain.
        nonce (int): The nonce used for Proof of Work.
        hash (str): The current block's hash.
    """

    def __init__(
        self,
        index: int,
        transactions: List[Transaction],
        timestamp: float,
        prev_hash: str,
        nonce: int = 0,
        hash: str = "",
    ) -> None:
        """
        Initializes a new block.

        Args:
            index (int): The position of the block in the blockchain.
            transactions (List[Transaction]): A list of transactions included in the block.
            timestamp (float): The time at which the block was created.
            prev_hash (str): The hash of the previous block in the blockchain.
            nonce (int, optional): The nonce used for Proof of Work. Defaults to 0.
            hash (str, optional): The current block's hash. Defaults to an empty string.
        """
        self.index: int = index
        self.transactions: List[Transaction] = transactions
        self.timestamp: float = timestamp
        self.prev_hash: str = prev_hash
        self.nonce: int = nonce
        self.hash: str = hash

    def calculate_hash(self) -> str:
        """
        Serializes block and calculates the SHA-256 hash of the block's contents.

        Returns:
            str: The computed hash of the block.
        """
        block_data = {
            "index": self.index,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "timestamp": self.timestamp,
            "prev_hash": self.prev_hash,
            "nonce": self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty: int) -> None:
        """
        Mines the block by finding a nonce that results in a hash meeting the difficulty criteria.

        Args:
            difficulty (int): The number of leading zeros required in the block's hash.
        """
        target = '0' * difficulty
        print(f"Minig block {self.index}...")
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block {self.index} mined {self.hash}")
