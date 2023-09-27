# Beneficial Assets Ownership (BAO) 

## Overview

Beneficial Asset Ownership (BAO) protocol aims at creating real-world utility on Blockchain by associating non-fungible tokens to crowd financing profitable projects, thereby creating value that can be distributed towards the token owners. The purpose of this document is to outline the high-level process of it including the stakeholders, execution, and required contract standards. BAO is a open source effort backed by [Hyperglade](https://hyperglade.com/product/).

## Contributing

You can help us extend the BAO protocol in 3 ways,
1. Implmenting use cases / examples using BAO procotol
2. Implementing the BAO protocl in other chains
3. Extending the BAO protocol

### Implmenting use cases / examples using BAO procotol

The goal of BAO is to provide an open protocol that builders can easily leverage and build for their own use cases. Currently at Hyperglade, we are using BAO for our own crowd-financing use case that allows funders across borders to invest in projects, and derive a long revenue out of it. If you are building a use case on top of an existing BAO contract, read on the [Usage section](#usage) for know more for more details. If you have a cool use case done using BAO, open a ticket with the subject "[Showcase] Your project title" for us to add it to our demo section.

### Implementing the BAO protocl in other chains

BAO is a chain agnostic protocol and only provides a generic specification. The specification needs to be implemented in each chain using chain-specific abstractions. This is similar to a ERC contract definition, and its implementation across different chains. Currently contracts for the following chains are available,

1. Tezos - Done by @TarunWebdev and the TZ APAC/India team

If you like to implement the same for a different chain (ex: Ethereum, Solana, etc), feel free to take a crack at it. Opening a ticket with the subject "[Contract] Implementing for X chain" helps us track the implementations. 

You can also provide updates to an existing contract. Please note that all updates should still map correctly to the specification. Updates can only be enhancements for the existing fundtionality. For instance, you could make a function more efficient in a contract - which will be considered as a correct update to the contract.

For contributing, please fork the repo and make the changes. Once you are ready, make a PR back to this repo with details on what you are changing, why, and possibly the improvements it provides.

### Extending the BAO protocol

Like any other protocol BAO needs to be updated at the protocol level to fit newer and better use cases. Protocol level updates will be done with a maximum frequency of 4 times a year. You are of course free to create your own version of the protocol by taking a fork. But the officil protocol specification will be kept in this repo.


## Usage

### Folder structure

`contracts` folder contains the chain native implementations of BAO.
`examples` folder contains web-apps, that are working samples of using one or more of the contracts above.

### How to create a use case

Creating a use case often involves creating the web2 counterpart of your use case and conectiong to the BAO protocol. A BAO contract is designed to be a single-use contract. Which means that for each instance that you need it to be run, you need a new contract deployed. This design was done intensionaly and we are hoping to update it to a contract factory method. For now follow these steps,

1. Deploy the contract
Find the implementation for your chain from the `contracts` folder and follow the README of that contract section for details on deploying it to the relevant chain.

2. Contract connector
Each chain would have a different way for your webapp/backend to the deployed contract. In the backend this is usually done through a relay node that lets you interact with the key-pair stored in your backend. In the frontend, this would be done using a SDK or a web3.js connector. Figure out which of these methods are used for your app. The `examples` folder can be a good starting point, especially for web apps.

