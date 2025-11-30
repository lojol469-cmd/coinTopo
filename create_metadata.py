import requests
import base64
import json
import os
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import Transaction
from solders.message import Message
from solders.system_program import CreateAccountParams, create_account
from solders.instruction import Instruction, AccountMeta
from spl.token.constants import TOKEN_PROGRAM_ID
from config import *

# Configuration Metaplex
METADATA_PROGRAM_ID = Pubkey.from_string("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")

def upload_logo_to_imgbb():
    """Upload logo to imgbb for temporary hosting"""
    api_key = "your_imgbb_api_key"  # Free API key from imgbb.com

    with open("topocoin_logo.png", "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    payload = {
        "key": api_key,
        "image": image_data
    }

    response = requests.post("https://api.imgbb.com/1/upload", data=payload)
    if response.status_code == 200:
        return response.json()["data"]["url"]
    else:
        # Fallback: use GitHub raw URL if available
        return "https://raw.githubusercontent.com/your-repo/topocoin_logo.png"

def create_metadata_instruction(mint_pubkey, wallet_pubkey, metadata_url):
    """Create the instruction to create metadata account"""

    # Derive metadata account address
    seeds = [
        b"metadata",
        bytes(METADATA_PROGRAM_ID),
        bytes(mint_pubkey)
    ]

    metadata_pda = Pubkey.find_program_address(seeds, METADATA_PROGRAM_ID)[0]

    # Metadata data
    metadata = {
        "name": "Topocoin",
        "symbol": "TPC",
        "uri": metadata_url,
        "sellerFeeBasisPoints": 0,
        "creators": None,
        "collection": None,
        "uses": None
    }

    # Serialize metadata
    metadata_json = json.dumps(metadata)
    metadata_bytes = metadata_json.encode('utf-8')

    # Create instruction data
    # create_metadata_accounts_v3 discriminator
    discriminator = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    # Instruction data: discriminator + metadata
    instruction_data = discriminator + metadata_bytes

    # Accounts
    accounts = [
        AccountMeta(pubkey=metadata_pda, is_signer=False, is_writable=True),
        AccountMeta(pubkey=mint_pubkey, is_signer=False, is_writable=False),
        AccountMeta(pubkey=wallet_pubkey, is_signer=True, is_writable=False),  # mint authority
        AccountMeta(pubkey=wallet_pubkey, is_signer=True, is_writable=False),  # payer
        AccountMeta(pubkey=wallet_pubkey, is_signer=True, is_writable=False),  # update authority
        AccountMeta(pubkey=Pubkey.from_string("SysvarRent111111111111111111111111111111111"), is_signer=False, is_writable=False),
    ]

    return Instruction(
        program_id=METADATA_PROGRAM_ID,
        accounts=accounts,
        data=instruction_data
    )

def main():
    client = Client(RPC_URL)

    # Load keypair
    with open(os.path.expanduser(KEYPAIR_PATH), "r") as f:
        data = json.load(f)
    keypair = Keypair.from_bytes(bytes(data))
    wallet_pubkey = keypair.pubkey()
    mint_pubkey = Pubkey.from_string(TOKEN_MINT)

    # Upload logo
    print("Uploading logo...")
    logo_url = upload_logo_to_imgbb()
    print(f"Logo URL: {logo_url}")

    # Create metadata JSON
    metadata = {
        "name": "Topocoin",
        "symbol": "TPC",
        "description": "Token Topocoin pour le projet Gabonextube",
        "image": logo_url,
        "external_url": "https://github.com/lojol469-cmd/GABONEXTUBE",
        "attributes": [
            {"trait_type": "Type", "value": "Utility Token"},
            {"trait_type": "Network", "value": "Solana Devnet"}
        ]
    }

    # For now, we'll use a data URL for the metadata
    metadata_json = json.dumps(metadata)
    metadata_b64 = base64.b64encode(metadata_json.encode()).decode()
    metadata_url = f"data:application/json;base64,{metadata_b64}"

    print(f"Metadata URL: {metadata_url}")

    # Create metadata instruction
    metadata_ix = create_metadata_instruction(mint_pubkey, wallet_pubkey, metadata_url)

    # Create transaction
    recent_blockhash = client.get_latest_blockhash().value.blockhash
    message = Message([metadata_ix], wallet_pubkey)
    transaction = Transaction([keypair], message, recent_blockhash)

    # Send transaction
    try:
        tx_sig = client.send_raw_transaction(bytes(transaction))
        print(f"Metadata créée avec succès !")
        print(f"Signature: {tx_sig.value}")

        # Vérifier
        print("Vérification de la metadata...")
        # Note: Pour vérifier, on peut utiliser un explorateur

    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    main()