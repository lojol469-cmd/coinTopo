import os
import json
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import Transaction
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import (
    get_associated_token_address,
    create_associated_token_account,
    mint_to,
    MintToParams,
)

# Configuration
RPC_URL = "https://api.devnet.solana.com"
KEYPAIR_PATH = os.path.expanduser("~/.config/solana/id_new.json")
TOKEN_MINT = "CS6yA2CBxyXUU1WV88SHwTL79ToUcySk4U3nQAgGErTg"
TOKEN_DECIMALS = 9

client = Client(RPC_URL)

# Load keypair
def load_keypair(path: str) -> Keypair:
    with open(path, "r") as f:
        data = json.load(f)
    return Keypair.from_bytes(bytes(data))

keypair = load_keypair(KEYPAIR_PATH)
wallet_pubkey = keypair.pubkey()
mint_pubkey = Pubkey.from_string(TOKEN_MINT)

# Test mint
amount_to_mint = 1.0
ata = get_associated_token_address(wallet_pubkey, mint_pubkey)
instructions = []

# Create ATA if needed
if client.get_account_info(ata).value is None:
    instructions.append(
        create_associated_token_account(
            payer=wallet_pubkey,
            owner=wallet_pubkey,
            mint=mint_pubkey
        )
    )

# Mint
instructions.append(
    mint_to(
        MintToParams(
            program_id=TOKEN_PROGRAM_ID,
            mint=mint_pubkey,
            dest=ata,
            mint_authority=wallet_pubkey,
            amount=int(amount_to_mint * 10**TOKEN_DECIMALS),
            signers=[]
        )
    )
)

from solders.message import Message

print("Instructions:", instructions)

try:
    recent_blockhash = client.get_latest_blockhash().value.blockhash
    message = Message(instructions, wallet_pubkey)
    transaction = Transaction([keypair], message, recent_blockhash)
    tx_sig = client.send_raw_transaction(bytes(transaction))
    print("Success:", tx_sig.value)
    print("Success:", tx_sig.value)
except Exception as e:
    import traceback
    print("Error:", e)
    traceback.print_exc()