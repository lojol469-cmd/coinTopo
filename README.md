# Topocoin Dashboard - Configuration et Tutoriels

Ce projet est un tableau de bord Streamlit pour gérer Topocoin (TPC) sur le Devnet Solana. Il permet de minter des tokens, envoyer des SOL et des TPC, et consulter les soldes.

## Prérequis

- **Système d'exploitation** : Linux (Ubuntu recommandé)
- **Python** : Version 3.8 ou supérieure (testé avec 3.13)
- **Solana CLI** : Version 1.18.22 ou supérieure
- **Connexion Internet** : Pour accéder au Devnet Solana

## Installation

### 1. Installation de Solana CLI

En raison de problèmes SSL, téléchargez directement depuis GitHub :

```bash
# Télécharger la release
wget --no-check-certificate https://github.com/solana-labs/solana/releases/download/v1.18.22/solana-release-x86_64-unknown-linux-gnu.tar.bz2

# Extraire
tar -xjf solana-release-x86_64-unknown-linux-gnu.tar.bz2

# Ajouter au PATH (ajoutez cette ligne à votre ~/.bashrc pour persister)
export PATH="$PWD/solana-release/bin:$PATH"

# Vérifier l'installation
solana --version
```

### 2. Configuration du Devnet

```bash
# Configurer pour Devnet
solana config set --url https://api.devnet.solana.com

# Vérifier la configuration
solana config get
```

### 3. Création du Wallet Principal

```bash
# Créer un nouveau keypair
solana-keygen new --outfile ~/.config/solana/id_new.json

# IMPORTANT : Sauvegardez la phrase seed affichée ! Elle permet de récupérer le wallet.
# Notez aussi l'adresse publique (Public key).
```

### 4. Airdrop de SOL (Devnet)

```bash
# Demander 2 SOL pour les frais de transaction
solana airdrop 2

# Vérifier le solde
solana balance
```

### 5. Création du Token Topocoin

```bash
# Créer le token mint
spl-token create-token --decimals 9

# Notez l'adresse du mint (Token Mint Address)

# Créer le compte associé (ATA) pour recevoir les tokens
spl-token create-account <TOKEN_MINT_ADDRESS>

# Minter 1 milliard de TPC initiaux
spl-token mint <TOKEN_MINT_ADDRESS> 1000000000

# Vérifier le solde de tokens
spl-token balance <TOKEN_MINT_ADDRESS>
```

### 6. Création du Wallet Test (Optionnel)

Pour tester les transferts en toute sécurité :

```bash
# Créer un wallet test
solana-keygen new --outfile ~/Topocoin/wallet_test.json

# Airdrop 1 SOL au wallet test
solana airdrop 1 --keypair ~/Topocoin/wallet_test.json

# Créer l'ATA pour le wallet test
spl-token create-account <TOKEN_MINT_ADDRESS> --owner ~/Topocoin/wallet_test.json
```

### 7. Installation des Dépendances Python

```bash
# Installer les packages requis
pip install streamlit solana spl-token-py base58
```

Ou utiliser le fichier requirements.txt :

```bash
pip install -r requirements.txt
```

## Configuration de l'Application

1. **Mettre à jour app.py** :
   - Remplacez `TOKEN_MINT` par votre adresse de mint
   - Vérifiez les chemins des keypairs

2. **Variables importantes** :
   - `TOKEN_MINT` : Adresse du token Topocoin
   - `TOKEN_DECIMALS` : 9 (décimales du token)
   - `KEYPAIR_PATH` : `~/.config/solana/id_new.json`
   - `TEST_KEYPAIR_PATH` : `~/Topocoin/wallet_test.json`

## Lancement de l'Application

```bash
# Depuis le dossier Topocoin
streamlit run app.py
```

L'application s'ouvrira dans votre navigateur à `http://localhost:8501`.

## Tutoriels d'Utilisation

### 1. Consultation des Soldes

- L'application affiche automatiquement les soldes SOL et TPC des wallets principal et test
- Actualisez la page pour voir les mises à jour

### 2. Mint de TPC

- Allez à la section "Mint TPC"
- Entrez la quantité à minter (ex: 1000)
- Cliquez sur "Mint TPC"
- Confirmez la transaction sur Devnet
- Vérifiez le solde mis à jour

### 3. Envoi de TPC vers le Wallet Test

- Section "Envoyer TPC vers le wallet test"
- Entrez la quantité à envoyer
- Cliquez sur "Envoyer au wallet test"
- La transaction crée automatiquement l'ATA si nécessaire

### 4. Envoi de SOL (si implémenté)

- Utilisez la section d'envoi SOL avec l'adresse du destinataire
- Entrez le montant en SOL
- Confirmez la transaction

## Dépannage

### Erreur SSL lors du téléchargement
- Utilisez `--no-check-certificate` avec wget

### Erreur de solde insuffisant
- Faites un airdrop supplémentaire : `solana airdrop 1`

### Erreur de keypair
- Vérifiez les chemins dans app.py
- Assurez-vous que les fichiers existent

### Erreur lors du mint
- Vérifiez que vous êtes l'autorité du mint
- Assurez-vous d'avoir assez de SOL pour les frais

### Application ne se lance pas
- Vérifiez que toutes les dépendances sont installées
- Vérifiez la version de Python

## Sécurité

- **Sauvegardez vos phrases seed** : Elles permettent de récupérer vos wallets
- **Ne partagez jamais vos keypairs** : Les fichiers .json contiennent vos clés privées
- **Utilisez le wallet test** pour expérimenter sans risque
- **Vérifiez les adresses** avant chaque transaction

## Structure du Projet

```
Topocoin/
├── app.py                 # Application Streamlit principale
├── config.py              # Configuration centralisée
├── create_logo.py         # Script de génération du logo
├── topocoin_logo.png      # Logo du projet
├── requirements.txt       # Dépendances Python
├── README.md             # Ce fichier
├── wallet_test.json      # Wallet de test (optionnel)
└── test_mint.py          # Script de test pour le mint
```

## Support

Pour toute question ou problème, vérifiez :
1. Les logs de la console Streamlit
2. Les messages d'erreur détaillés
3. La documentation Solana officielle
4. Les forums de la communauté Solana

## Mises à Jour

- Gardez Solana CLI à jour
- Vérifiez les mises à jour des dépendances Python
- Consultez les changements sur le Devnet Solana

## Passage en Production (Mainnet)

### Pourquoi passer sur Mainnet ?

- **Devnet** : Réseau de test, tokens sans valeur réelle
- **Mainnet** : Réseau principal, tokens avec valeur réelle si adoptés

### Instructions pour Mainnet

1. **Préparation :**
   ```bash
   # Achetez des SOL sur un exchange (Binance, Coinbase, etc.)
   # Utilisez le même wallet que pour Devnet (même adresse, soldes séparés)
   
   # Vérifiez votre adresse actuelle
   solana address
   
   # Sauvegardez votre phrase seed si ce n'est pas déjà fait !
   ```

2. **Configuration :**
   - Modifiez `config.py` :
     ```python
     DEFAULT_NETWORK = 'mainnet'
     # Gardez le même KEYPAIR_PATH que pour Devnet
     ```
   - Votre adresse wallet reste la même :
     ```bash
     solana address
     ```

3. **Transfert de SOL :**
   - Envoyez des SOL réels vers votre wallet Mainnet
   - Minimum recommandé : 0.1 SOL pour les frais

4. **Création du token sur Mainnet :**
   ```bash
   # Configuration Mainnet
   solana config set --url mainnet-beta
   
   # Créer le token
   spl-token create-token --decimals 9
   
   # Notez la nouvelle adresse MINT
   # Mettez à jour TOKEN_MINT dans config.py
   ```

5. **Configuration finale :**
   - Mettez à jour `TOKEN_MINT` dans `config.py`
   - Créez les comptes associés
   - Minter les tokens initiaux

### ⚠️ Avertissements Mainnet

- **Coûts réels** : Toutes les transactions coûtent des SOL
- **Irréversible** : Les transactions ne peuvent pas être annulées
- **Sécurité** : Sauvegardez vos clés privées et phrases seed
- **Tests** : Testez d'abord toutes les fonctionnalités sur Devnet

### Interface de l'Application

L'application inclut maintenant un sélecteur de réseau dans la barre latérale :
- **Devnet** : Pour les tests
- **Mainnet** : Pour la production

Sur Mainnet, des avertissements de sécurité s'affichent automatiquement.