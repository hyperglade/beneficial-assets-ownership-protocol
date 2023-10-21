BAO Contract for Tezos
======================

This folder contains the latest implementation of BAO specification in SmartPy for Tezos. Below are the intructions for compiling, deploying, and using it.

## Tools setup
1. Installing Temple wallet
2. Creating wallets for each user
3. Using https://better-call.dev/
4. Add Tezos using the faucet: https://faucet.ghostnet.teztnets.xyz/
5. Add USDt usng the faucet: https://faucet.marigold.dev/

## Compiling

1. Install SmartPY legal CLI from https://legacy.smartpy.io/docs/cli#cli
2. Once installed, use the command below to compile the contract
`smartpy test BAOProtocol.py ./build/`

## Deploying contract
1. Goto https://better-call.dev/ and select "Deploy"
2. Upload the file named `step_004_cont_1_contract.tz`
3. Set the following initial variable

```
administrator -> Wallet address of the Protocol Owner
protocolOwner -> Wallet address of the Protocol Owner
protocolStatus -> INACTIVE
facilitator -> None
projectOwner -> None
metadata -> 697066733a2f2f6261666b726569657a647a6465773374667078766a78727166676c6236777a67796570777567617274707a66746b72736c6d646f6c707165346f75
token -> KT1WNrZ7pEbpmYBGPib1e7UVCeC6GA6TkJYR
```

4. Make sure the wallet of the Protocol Owner is active in Templte
5. Use Deploy to deploy the contract
6. Use the contract address provided in the transaction
7. You can use better-dev to interact with the deployed contract or use the provided web app.

## Using the web app

1. Demo web app for the contract is available in `examples/tezos-contract-demo`
2. Use `npm install` or `yarn install` to install the packages
3. Use `npm run dev` or `yarn dev` to start the web app
4. Update the Contract Address field to the address of the contract created earlier. This will now show the current contract status. You can now go through the BAO protocol steps.
5. Use 'Connect Wallet' and connect your Protocol Owner wallet first
6. Set the facilitator
7. Set the project owner
8. Init
Decimals are 6, so amount x 1000000
Min Payout is 0.0001 USDT


https://faucet.marigold.dev/


## Smart Contract (contract)

The `contract` folder contains the code for a smart contract written in SmartPy. This smart contract is designed to [briefly describe the purpose of the smart contract]. Below are some key details about the contract:

- **File**: `BAOProtocol.py`
- **Description**: `Smarpty Code for BAO Protocol.`


https://onlinestringtools.com/convert-string-to-bytes
https://tezostaquito.io/
