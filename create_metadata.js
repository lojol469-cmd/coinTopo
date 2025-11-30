const { Connection, Keypair, PublicKey, Transaction, sendAndConfirmTransaction } = require('@solana/web3.js');
const { createCreateMetadataAccountV3Instruction } = require('@metaplex-foundation/mpl-token-metadata');
console.log('Function available:', typeof createCreateMetadataAccountV3Instruction);
const fs = require('fs');
const path = require('path');
const os = require('os');

// Configuration
const RPC_URL = 'https://api.devnet.solana.com';
const KEYPAIR_PATH = path.join(os.homedir(), '.config', 'solana', 'id_new.json');
const TOKEN_MINT = 'CS6yA2CBxyXUU1WV88SHwTL79ToUcySk4U3nQAgGErTg';

// Metaplex Token Metadata Program ID
const PROGRAM_ID = new PublicKey('metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s');

async function main() {
    // Connection
    const connection = new Connection(RPC_URL, 'confirmed');

    // Load keypair
    const keypairData = JSON.parse(fs.readFileSync(KEYPAIR_PATH, 'utf8'));
    const keypair = Keypair.fromSecretKey(new Uint8Array(keypairData));
    const walletPublicKey = keypair.publicKey;

    // Mint public key
    const mintPublicKey = new PublicKey(TOKEN_MINT);

    // Load metadata
    const metadataPath = path.join(__dirname, 'metadata.json');
    const metadata = JSON.parse(fs.readFileSync(metadataPath, 'utf8'));

    // Create metadata URI (data URL)
    const metadataUri = `data:application/json;base64,${Buffer.from(JSON.stringify(metadata)).toString('base64')}`;

    console.log('Metadata URI:', metadataUri);

    // Create metadata account
    const [metadataPDA] = PublicKey.findProgramAddressSync(
        [
            Buffer.from('metadata'),
            PROGRAM_ID.toBuffer(),
            mintPublicKey.toBuffer(),
        ],
        PROGRAM_ID
    );

    console.log('Metadata PDA:', metadataPDA.toString());

    // Create instruction
    const createMetadataInstruction = createCreateMetadataAccountV3Instruction(
        {
            metadata: metadataPDA,
            mint: mintPublicKey,
            mintAuthority: walletPublicKey,
            payer: walletPublicKey,
            updateAuthority: walletPublicKey,
        },
        {
            createMetadataAccountArgsV3: {
                data: {
                    name: metadata.name,
                    symbol: metadata.symbol,
                    uri: metadataUri,
                    sellerFeeBasisPoints: 0,
                    creators: null,
                    collection: null,
                    uses: null,
                },
                isMutable: true,
                collectionDetails: null,
            },
        }
    );

    // Create transaction
    const transaction = new Transaction().add(createMetadataInstruction);
    const { blockhash } = await connection.getLatestBlockhash();
    transaction.recentBlockhash = blockhash;
    transaction.feePayer = walletPublicKey;

    // Sign and send
    try {
        const signature = await sendAndConfirmTransaction(connection, transaction, [keypair]);
        console.log('Metadata créée avec succès !');
        console.log('Signature:', signature);
        console.log('Metadata Account:', metadataPDA.toString());
    } catch (error) {
        console.error('Erreur:', error);
    }
}

main().catch(console.error);