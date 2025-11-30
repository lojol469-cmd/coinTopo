# Configuration Topocoin
# Fichier de configuration pour les paramètres sensibles

# Réseaux disponibles
NETWORKS = {
    'devnet': {
        'rpc': 'https://api.devnet.solana.com',
        'name': 'Devnet (Test)',
        'explorer': 'https://explorer.solana.com',
        'faucet': 'https://faucet.solana.com'
    },
    'mainnet': {
        'rpc': 'https://api.mainnet-beta.solana.com',
        'name': 'Mainnet (Production)',
        'explorer': 'https://explorer.solana.com',
        'faucet': None
    }
}

# Réseau par défaut
DEFAULT_NETWORK = 'devnet'

# URLs
RPC_URL = NETWORKS[DEFAULT_NETWORK]['rpc']

# Chemins des keypairs
KEYPAIR_PATH = "~/.config/solana/id_new.json"
TEST_KEYPAIR_PATH = "~/Topocoin/wallet_test.json"

# Token
TOKEN_MINT = "CS6yA2CBxyXUU1WV88SHwTL79ToUcySk4U3nQAgGErTg"
TOKEN_DECIMALS = 9

# Interface
PAGE_TITLE = "Topocoin Dashboard"
LAYOUT = "centered"