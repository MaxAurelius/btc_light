from typing import List
from transactions import Transaction


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
        previous_hash: str,
        nonce: int = 0,
        hash: str = "",
    ) -> None:
        """
        Initializes a new block.

        Args:
            index (int): The position of the block in the blockchain.
            transactions (List[Transaction]): A list of transactions included in the block.
            timestamp (float): The time at which the block was created.
            previous_hash (str): The hash of the previous block in the blockchain.
            nonce (int, optional): The nonce used for Proof of Work. Defaults to 0.
            hash (str, optional): The current block's hash. Defaults to an empty string.
        """
        self.index: int = index
        self.transactions: List[Transaction] = transactions
        self.timestamp: float = timestamp
        self.previous_hash: str = previous_hash
        self.nonce: int = nonce
        self.hash: str = hash

    def calculate_hash(self) -> str:
        """
        Calculates the SHA-256 hash of the block's contents.

        Returns:
            str: The computed hash of the block.
        """
        pass  # Implementation will go here

    def mine_block(self, difficulty: int) -> None:
        """
        Mines the block by finding a nonce that results in a hash meeting the difficulty criteria.

        Args:
            difficulty (int): The number of leading zeros required in the block's hash.
        """
        pass  # Implementation will go here

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
        pass  # Implementation will go here

    def get_latest_block(self) -> Block:
        """
        Retrieves the latest block in the blockchain.

        Returns:
            Block: The most recent block.
        """
        pass  # Implementation will go here

    def add_block(self, new_block: Block) -> None:
        """
        Adds a new block to the blockchain after validating it.

        Args:
            new_block (Block): The block to be added.
        """
        pass  # Implementation will go here

    def is_chain_valid(self) -> bool:
        """
        Validates the integrity of the entire blockchain.

        Returns:
            bool: True if the blockchain is valid, False otherwise.
        """
        pass  # Implementation will go here

    def add_transaction(self, transaction: Transaction) -> None:
        """
        Adds a new transaction to the mempool after verification.

        Args:
            transaction (Transaction): The transaction to be added.
        """
        pass  # Implementation will go here

    def mine_pending_transactions(self, miner_address: str) -> None:
        """
        Mines all pending transactions, adds them to a new block, and rewards the miner.

        Args:
            miner_address (str): The address of the miner to receive the block reward.
        """
        pass  # Implementation will go here