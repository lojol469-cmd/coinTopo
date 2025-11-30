#!/bin/bash

# Setup script for new Topocoin on Devnet

# Add Solana to PATH (assuming extracted in home)
export PATH="$HOME/solana-release/bin:$PATH"

echo "Creating new wallet..."
solana-keygen new -o ~/.config/solana/id_new.json --no-passphrase

echo "Configuring Solana for Devnet..."
solana config set --keypair ~/.config/solana/id_new.json
solana config set --url https://api.devnet.solana.com

echo "Requesting airdrop..."
solana airdrop 5

echo "Checking balance..."
solana balance

echo "Creating new token..."
TOKEN_MINT=$(spl-token create-token --decimals 9 --owner ~/.config/solana/id_new.json | grep "Creating token" | awk '{print $3}')

echo "Token Mint Address: $TOKEN_MINT"

echo "Creating token account..."
spl-token create-account $TOKEN_MINT

echo "Minting initial supply..."
spl-token mint $TOKEN_MINT 1000000000

echo "Setup complete. Save the keypair file and seed phrase securely."
echo "Update your app with TOKEN_MINT=$TOKEN_MINT"