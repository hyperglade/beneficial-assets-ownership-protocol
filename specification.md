BAO Protocol Specification
==========================

Beneficial Asset Ownership (BAO) protocol aims at creating real-world utility on Blockchain by associating non-fungible tokens to crowd financing profitable projects, thereby creating value that can be distributed towards the token owners. The purpose of this document is to outline the high-level process of it including the stakeholders, execution, and required contract standards.

## Abstract


## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

### Definitions

- Facilitator
A trusted entity that is responsible for vetting the Projects and the Project Owners. The facilitator should be a known entity. Responsibilities include,
    - KYC of the Project Owner
    - Initiating legal action on an event of a rug-pull
    - Maintaining the integrity of the Project
- Protocol Owner
An entity that’s being employed by the Facilitator for the purpose of deploying the protocol. The Protocol Owner needs to possess the technical know-how and the depth of running the protocol. Facililator and Protocol owner can be the same entity.
- Project
A real-world project/event/asset that could generate revenue in the longer term.
- Project Owner
A person or an entity that managed the Project prospectus and operationally carry out the Project nitigrities.
- NFT Contract
The ERC-721 contract that will be used for crowdfinancing for the Project
- NFT Holder
Minters/Holders/Purchasers of the NFT Contract that’s being used for crowdfinancing the Project
- Treasury
    - Funding Wallet
    Contract wallet in which all NFT mint proceeds are collected.
    - Distribution Wallet
    Contract wallet in which all rewards/revenue from the Project is sent to. These funds will be distributed to the NFT holders depending on the ownership structure.
    - Project Owner Stake
    The Project Owner is required to stake a certain percentage of the total funding requirement as insurance. The percentage is determined by the Facilitator.

### Working Model

1. Project Owner onboarding
The BAO protocol is initiated on the request for crowdfunding by a Project Owner towards a Facilitator. Project Owner and the Faciliator MUST be unrelated entities. The Facilitator is required to carry-out thorough KYC process to determine the authenticity of the Project Owner and the proposed Project prospectus. 
Facilitator is also required to arrange a binding legal contract in the relevant jurisdiction with the Project Owner.

3. Project funding limit 
The Facilitator is required to determine the initial funding limit for the Project Owner. This is on the sole discretion of the Facilitator and must be defined in the contract.

5. Project specification
The Project Owner is required to prepare a comprehensive Project prospectus outlining the fund utilization, expect revenue means, and associated risks.

7. Protocol deployment
The Protocol Owner is employed by the Facilitator to deploy the BAO contract along with the relevant parameters to carry out the crowdfunding process. The Facilitator and the Protocol Owner CAN be the same entity.

9. NFT mint
Initial NFT mint is carried out for fund collection by the Protocol Owner. The criteria for a successful funding needs to be set in the contract. If the funding criteria is met, the funding will be dispersed to the Project Owner by the contract.

11. Project execution
The Project Owner is required to carry out the Project as defined and provide updates off-chain the NFT holders.

13. Reward accumiltion
The Project Owner is required to send revenue proceeds from the Project to the distribution wallet of the contract. Funds accumulated as proceeds are dispersed to the NFT holder wallets by the contract.

15. Fund distribution
Fund distribution is carried out as per the specified percentages of the contract.
    1. x% of each fund distribution to be allocated for the Facilitator
    2. y% of each fund distribution to be allocated for the Project Owner
    3. z% of each fund distribution to be allocated for the Protocol Owner
    4. Remaining majority of the funds to be distributed to the NFT Holders
       
16. Rugpull Safeguard
In the event of a fraudulent Project Owner, the Facilitator is required to take required legal measures to recover at best the funding acquired for the Project. The Project Owner’s stake can be used for carrying out the legal actions. Recovered funding needs to be deposited to the distribution wallet of the contract to be dispersed towards the NFT Holders.

### Contract Specification

The BAO protocol standard is dictated by the following specification.

```javascript

interface BAOProtocol{
    
    // Track the state of the protocol lifecycle
    var protcolStatus;

    // Address of the user that deployed the contract
    // Hardcoded address at deployment
    var protocolOwner;

    // Address of the user that's facilitating the protocol deployment
    var facilitator;

    // Address of the project owner of the project
    var projectOwner;

    // Addresses of the funders
    // Ex: If NFT mint is the funding source, this should correspond to the ownership
    // index in the NFT contract
    var funders[];

    // Treasury for fund collection proceeds
    // Ex: NFT mint treasury if funding is done through a NFT mint
    var collectionTreasury;

    // Treasury for fund distribution proceeds
    var distributionTreasury;

    // Project owner's stake for liability risks. This can be withdrawn to the
    // facilitator's wallet at any point of protcol execution
    var projectOwnerStake;

    /** Project related parameters **/

    // Methods of funding, currently supported { NFT_MINT,  }
    var fundingMethod;

    // This is an optional propery. If funding is by NFT_MINT, this stores the 
    // NFT contract address
    var fundingMethodContract;
    
    // Total funding amount expected to be raised
    var fundingAmount;

    // Percentage of funds that needs to be raised at MINIMUM for the funds to be unlocked
    // to the project owner
    var minRaisePercentage;

    // Amount that the project owner need to stake in the contract for liability
    var projectOwnerStakeRequirement;

    // Portion of the project to be given to the project owner
    // If the project owner gets his cut beforehand, this can be 0%
    var projectOwnerRevenuePercentage;

    // Portion of the project to be given to the facilitator
    var faciliatatorRevenuePercentage;

    // Portion of the project to be given to the funders
    var funderRevenuePercentage;

    // Portion of the project to be given to the protocol owner
    var protocolOwnerRevenuePercentage;

    /**
     * Setter for the facilitator addressl
     * Invoked by: Protocol Owner
     * @_facilitator Faciliator's address
     * 
    **/
    function setFacilitator(_facilitator);
    
    /**
     * Function to initialize the protocol
     * Invoked by: Facilitator
     * @_projectOwner Faciliator's address
     * @_fundingAmount
     * @_minRaisePercentage
     * @_projectOwnerStakeRequirement
     * 
    **/
    function init(_projectOwner, _fundingAmount, _minRaisePercentage _projectOwnerStakeRequirement, _projectOwnerRevenuePercentage, _faciliatatorRevenuePercentage, _funderRevenuePercentage, _protocolOwnerRevenuePercentage);

    /**
     * Function to set the funding method
     * Let's see how we use this with a ERC-721 NFT contract
     * There are 2 possible ways
     * ---- 01: Extending the BAO contract to ERC-721 so that BAO can facilitate the mint
     *          This allows BAO contract to natively keep track of the minters, and related details
     * 
     * ---- 02: Use a custom ERC-721 contract for minting that invokes the BAO contract methods
     *          This decouples BAO from the NFT contract, but the NFT contract needs to be 
     *          custom created to make sure it invokes the relevant BAO functions
     * Invoked by: Facilitator
    **/
    function setFundingMethod(_fundingMethod, _fundingMethodContract);

    /**
     * Function to stake the amount required by the project owner
     * Validates if the amount sent by project owner matched the projectOwnerStakeRequirement
     * Once stake is complete, the protocol status is ACTIVE
     * Invoked by: Project Owner
    **/
    function stake() payable;

    /**
     * Function to withdraw the collected funds to the project owner's wallet
     * Once the withdraw is compelte, the protocol status is FUNDED
     * TODO: Introduce tranching regulated by the facilitators
     * Invoked by: Project Owner
    **/
    function withdrawFunds() payable;

    /**
     * Function to add funds to the distributionTreasury
     * Project owner needs to be invoke this from their wallet with any specific amount of funds
     * Funds has to be tokens in the relevant blockchain
     * Preferred to be USDC given it's token implementations across many chains
     * Invoked by: Project Owner
    **/
    function collectRevenue() payable;

    /**
     * Function to distribute the collected revenue to the NFT holders
     * All funds collectd in distributionTreasury will be distributed as below,
     * - Facilitator: faciliatatorRevenuePercentage x distributedTreasury
     * - Project Owner: projectOwnerRevenuePercentage x distributedTreasury
     * - Protocol Owner: protocolOwnerRevenuePercentage x distributedTreasury
     * - Each Funder: funderRevenuePercentage x distributedTreasury / funders
     * Invoked by: Facilitator 
    **/
    function payout() payable;

    /**
     * Function to cancel the protocol and return all funds to the funders
     * This can ONLY be invoked in the ACTIVE stage or earlier
     * Project owner's stake will be returned as well
     * Invoked by: Facilitator
    **/
    function dissolve();
}

```

