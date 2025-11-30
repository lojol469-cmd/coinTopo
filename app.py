import streamlit as st
import os
import json
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import Transaction
from solders.message import Message
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import (
    get_associated_token_address,
    create_associated_token_account,
    transfer_checked,
    mint_to,
    MintToParams,
    TransferCheckedParams,
)
from config import *

from config import *

# ===================== CONFIGURATION =====================
# Configuration chargée depuis config.py
KEYPAIR_PATH = os.path.expanduser(KEYPAIR_PATH)
TEST_KEYPAIR_PATH = os.path.expanduser(TEST_KEYPAIR_PATH)

# Interface réseau
st.sidebar.title("🌐 Configuration Réseau")

network = st.sidebar.selectbox(
    "Sélectionner le réseau",
    options=list(NETWORKS.keys()),
    format_func=lambda x: NETWORKS[x]['name'],
    index=list(NETWORKS.keys()).index(DEFAULT_NETWORK)
)

# Mettre à jour la configuration selon le réseau
current_network = NETWORKS[network]
RPC_URL = current_network['rpc']

# Client RPC
client = Client(RPC_URL)

# Avertissement Mainnet
if network == 'mainnet':
    st.sidebar.warning("⚠️ **MAINNET - ATTENTION !**")
    st.sidebar.write("Vous êtes sur le réseau principal.")
    st.sidebar.write("- Les transactions coûtent de vrais SOL")
    st.sidebar.write("- Les tokens ont une valeur réelle")
    st.sidebar.write("- Sauvegardez vos clés privées !")
    st.sidebar.write("- Vérifiez les adresses avant chaque transaction")

    # Vérifier si le token existe sur Mainnet
    try:
        mint_info = client.get_account_info(Pubkey.from_string(TOKEN_MINT))
        if mint_info.value is None:
            st.sidebar.error("❌ Le token n'existe pas sur Mainnet")
            st.sidebar.info("Pour publier sur Mainnet, suivez les instructions ci-dessous")
        else:
            st.sidebar.success("✅ Token trouvé sur Mainnet")
    except:
        st.sidebar.error("Erreur de vérification du token")

# Informations réseau
st.sidebar.write(f"**RPC:** {RPC_URL}")
if current_network['faucet']:
    st.sidebar.write(f"**Faucet:** {current_network['faucet']}")
st.sidebar.write(f"**Explorer:** {current_network['explorer']}")

# Section Publication Mainnet
if network == 'devnet':
    with st.sidebar.expander("🚀 Publier sur Mainnet"):
        st.write("Pour rendre votre token réel :")
        st.write("1. **Utilisez le même wallet** (adresse identique)")
        st.write("2. **Basculez vers Mainnet** ci-dessus")
        st.write("3. **Achetez des SOL réels** et transférez-les")
        st.write("4. **Recréez le token** sur Mainnet (nouvelle adresse)")
        st.write("5. **Mettez à jour TOKEN_MINT** dans config.py")
        st.write("")
        st.warning("💰 **Coûts :** ~0.01 SOL pour créer le token")
        st.info("🔑 **Wallet :** Utilisez le même keypair, seule l'adresse importe")
        if st.button("Instructions détaillées", key="mainnet_instructions"):
            st.info("""
            **Étapes pour publier sur Mainnet :**
            
            1. **Préparation :**
               - Gardez le même wallet (pas besoin d'en créer un nouveau)
               - Achetez des SOL sur un exchange (Binance, Coinbase, etc.)
               - Transférez les SOL vers votre adresse existante :
                 `{wallet_pubkey}`
            
            2. **Configuration :**
               - Basculez vers Mainnet dans la barre latérale
               - Votre wallet Devnet fonctionne aussi sur Mainnet
               - Les adresses sont identiques sur tous les réseaux
            
            3. **Création du token sur Mainnet :**
               ```bash
               # Configuration Mainnet
               solana config set --url mainnet-beta
               solana address  # Vérifiez que c'est la bonne adresse
               
               # Créer le token
               spl-token create-token --decimals 9
               
               # Notez la NOUVELLE adresse MINT (différente de Devnet)
               # Mettez à jour TOKEN_MINT dans config.py avec cette adresse
               
               # Créer le compte associé
               spl-token create-account <NOUVELLE_MINT_ADDRESS>
               
               # Minter les tokens initiaux
               spl-token mint <NOUVELLE_MINT_ADDRESS> 1000000000
               ```
            
            4. **Sécurité :**
               - Sauvegardez vos phrases seed (même pour Mainnet)
               - Testez d'abord toutes les fonctionnalités sur Devnet
               - Vérifiez toutes les transactions sur Mainnet
               - Les frais sont en SOL réels !
            
            5. **Mise à jour de l'app :**
               - Modifiez `config.py` : `TOKEN_MINT = "nouvelle_adresse_mint"`
               - L'app détectera automatiquement le réseau
            """)

# ===================== CHARGEMENT DES CLÉS =====================
def load_keypair(path: str) -> Keypair:
    if not os.path.exists(path):
        st.error(f"Fichier introuvable : {path}")
        st.stop()
    with open(path, "r") as f:
        data = json.load(f)
    return Keypair.from_bytes(bytes(data))

try:
    keypair = load_keypair(KEYPAIR_PATH)
    wallet_pubkey = keypair.pubkey()

    test_keypair = load_keypair(TEST_KEYPAIR_PATH)
    test_pubkey = test_keypair.pubkey()
except Exception as e:
    st.error(f"Erreur de chargement des clés : {e}")
    st.stop()

mint_pubkey = Pubkey.from_string(TOKEN_MINT)

# ===================== VÉRIFICATION DU TOKEN =====================
token_exists = True
try:
    mint_info = client.get_account_info(mint_pubkey)
    token_exists = mint_info.value is not None
except:
    token_exists = False

# ===================== FONCTIONS UTILITAIRES =====================
def sol_balance(pubkey: Pubkey) -> float:
    return client.get_balance(pubkey).value / 1e9

def tpc_balance(pubkey: Pubkey) -> float:
    ata = get_associated_token_address(pubkey, mint_pubkey)
    try:
        resp = client.get_token_account_balance(ata)
        return int(resp.value.amount) / (10 ** TOKEN_DECIMALS)
    except:
        return 0.0

# ===================== INTERFACE =====================
st.title(f"{PAGE_TITLE} – {current_network['name']}")

# Afficher le logo
logo_path = os.path.join(os.path.dirname(__file__), "topocoin_logo.png")
st.image(logo_path, width=200)

# Informations du token
col_logo, col_info = st.columns([1, 2])
with col_logo:
    st.write("")
with col_info:
    st.subheader("🪙 Topocoin (TPC)")
    st.write(f"**Adresse :** `{TOKEN_MINT}`")
    if token_exists:
        explorer_link = f"{current_network['explorer']}/address/{TOKEN_MINT}?cluster={network}"
        st.write(f"**Explorer :** [🔍 Voir sur {current_network['name']}]({explorer_link})")
    st.write(f"**Décimales :** {TOKEN_DECIMALS}")
    st.write(f"**Réseau :** {current_network['name']}")

st.subheader("Soldes actuels")
col1, col2 = st.columns(2)

with col1:
    st.write("**Wallet Principal**")
    st.write(f"Adresse : `{wallet_pubkey}`")
    st.write(f"SOL : **{sol_balance(wallet_pubkey):.4f}** SOL")
    st.write(f"TPC : **{tpc_balance(wallet_pubkey):,.2f}** TPC")
    if token_exists:
        explorer_link = f"{current_network['explorer']}/address/{wallet_pubkey}?cluster={network}"
        st.write(f"[🔍 Explorer]({explorer_link})")

with col2:
    st.write("**Wallet Test**")
    st.write(f"Adresse : `{test_pubkey}`")
    st.write(f"SOL : **{sol_balance(test_pubkey):.4f}** SOL")
    st.write(f"TPC : **{tpc_balance(test_pubkey):,.2f}** TPC")
    if token_exists:
        explorer_link = f"{current_network['explorer']}/address/{test_pubkey}?cluster={network}"
        st.write(f"[🔍 Explorer]({explorer_link})")

# ===================== MINT TPC (seulement wallet principal) =====================
st.header("Mint TPC (uniquement wallet principal)")

if not token_exists:
    if network == 'mainnet':
        st.error("❌ Le token Topocoin n'existe pas sur Mainnet")
        st.info("Suivez les instructions dans la barre latérale pour créer le token sur Mainnet")
        st.stop()
    else:
        st.warning("⚠️ Token non trouvé - Vérifiez la configuration")

if token_exists:
    amount_to_mint = st.number_input(
        "Quantité de TPC à mint",
        min_value=0.0,
        step=1.0,
        key="mint_amount"
    )

    if st.button("Mint TPC", type="primary"):
        if amount_to_mint <= 0:
            st.error("La quantité doit être supérieure à 0")
        else:
            with st.spinner("Mint en cours…"):
                try:
                    ata = get_associated_token_address(wallet_pubkey, mint_pubkey)
                    instructions = []

                    # Créer l'ATA si elle n'existe pas
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

                    recent_blockhash = client.get_latest_blockhash().value.blockhash
                    message = Message(instructions, wallet_pubkey)
                    transaction = Transaction([keypair], message, recent_blockhash)
                    tx_sig = client.send_raw_transaction(bytes(transaction))
                    st.success(f"{amount_to_mint:,.2f} TPC mintés avec succès !")
                    st.code(tx_sig.value, language="text")
                except Exception as e:
                    st.error(f"Erreur lors du mint : {e}")
else:
    st.info("Token non disponible sur ce réseau")

# ===================== ENVOYER TPC VERS WALLET TEST =====================
st.header("Envoyer TPC vers le wallet test")

send_amount = st.number_input(
    "Quantité de TPC à envoyer",
    min_value=0.0,
    step=0.1,
    key="send_amount"
)

if st.button("Envoyer au wallet test", type="primary"):
    if send_amount <= 0:
        st.error("La quantité doit être supérieure à 0")
    else:
        with st.spinner("Transfert en cours…"):
            try:
                sender_ata = get_associated_token_address(wallet_pubkey, mint_pubkey)
                dest_ata = get_associated_token_address(test_pubkey, mint_pubkey)
                instructions = []

                # Créer l'ATA du destinataire si besoin
                if client.get_account_info(dest_ata).value is None:
                    instructions.append(
                        create_associated_token_account(
                            payer=wallet_pubkey,
                            owner=test_pubkey,
                            mint=mint_pubkey
                        )
                    )

                # Transfert avec transfer_checked (compatible Token-2022)
                instructions.append(
                    transfer_checked(
                        TransferCheckedParams(
                            program_id=TOKEN_PROGRAM_ID,
                            source=sender_ata,
                            mint=mint_pubkey,
                            dest=dest_ata,
                            owner=wallet_pubkey,
                            amount=int(send_amount * 10**TOKEN_DECIMALS),
                            decimals=TOKEN_DECIMALS,
                            signers=[]
                        )
                    )
                )

                recent_blockhash = client.get_latest_blockhash().value.blockhash
                message = Message(instructions, wallet_pubkey)
                transaction = Transaction([keypair], message, recent_blockhash)
                tx_sig = client.send_raw_transaction(bytes(transaction))
                st.success(f"{send_amount:,.2f} TPC envoyés au wallet test !")
                st.code(tx_sig.value, language="text")
            except Exception as e:
                st.error(f"Erreur lors du transfert : {e}")

st.caption(f"Dashboard Topocoin • {current_network['name']} • 2025")