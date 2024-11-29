from .transactions import Transaction
from .block import Block
from typing import List
from datetime import datetime, timezone


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

        if transaction.verify_signature():
            sender_address = transaction.sender_address
            if sender_address == "Network":
                self.mempool.append(transaction)
                print("Reward transaction added to mempool.")
                return

            sender_balance = self.get_balance(transaction.sender_address)
            if sender_balance >= transaction.amount:
                self.mempool.append(transaction)
                print("Transaction added to mempool")
            else:
                print(f"Senders balance is not sufficient {sender_balance}. Transaction rejected.")
        else:
            print("Invalid transaction signature. Transaction rejected.")

    def mine_pending_transactions(self, miner_address: str) -> None:
        """
        Mines all pending transactions, adds them to a new block, and rewards the miner.

        Args:
            miner_address (str): The address of the miner to receive the block reward.
        """
        
        if not self.mempool:
            print("No transactions to mine.")
            return
        
        # Create reward transaction for the miner
        reward_tx = Transaction(
            sender_address="Network",
            recipient_address=miner_address,
            amount=self.block_reward
        )

        # No need to sign reward tx as it's generated by the network

        # Add the reward transaction to the mempool
        self.mempool.append(reward_tx)

        # Create a new block with all transactions in the mempool
        new_block = Block(
            index = len(self.chain),
            transactions=self.mempool.copy(),
            timestamp=datetime.now(timezone.utc).isoformat(),
            prev_hash=self.get_latest_block().hash
        )

        # Mine the new block
        new_block.mine_block(self.difficulty)

        # Add the mined block to the blockchain
        self.chain.append(new_block)
        print(f"Block {new_block.index} has been added to the blockchain.")

        self.mempool.clear()

    def get_balance(self, address:str) -> float:
        """
        Calculates the balance of a given wallet address by aggregating transactions.
        Simple account-based model.

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