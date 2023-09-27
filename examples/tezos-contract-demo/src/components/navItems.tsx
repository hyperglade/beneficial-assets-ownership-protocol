export const navItems = [
    {
      name: 'Contract Overview',
      actions: [
       {
            name: 'contractOverview',
            entrypoint: 'null',
            payable: false,
            fields:[]
       }
      ],
    },
    {
      name: 'Protocol Owner Actions',
      actions: [
        { 
            name: 'Set Facilitator',
            entrypoint: 'setFacilitator',
            payable: false,
            fields: [
                { label: 'Facilitator', name: '_facilitator' ,placeholder:"Facilitator wallet address" },
            ]
        },
      ],
    },
    {
      name: 'Facilitator Actions',
      actions: [
        {
            name: 'Initialise Protocol',
            entrypoint: 'initProtocol',
            payable: false,
            fields: [
                { label: 'Project Owner', name: '_projectOwner' ,placeholder:"Project Owner wallet address" },
                { label: 'Funding Amount', name: '_fundingAmount' , placeholder:"1000000" },
                { label: 'Minting Price', name: '_mintingPrice' , placeholder:"1000000" },
                { label: 'Minimum Funds Required Percentage', name: '_minRaisePercentage' , placeholder:"50%" },
                { label: 'Staking Required', name: '_projectOwnerStakeRequirement' , placeholder:"1000000" },
                { name: "Revenue Percentage", heading: true },
                { label: 'Protocol Owner', name: '_protocolOwnerRevenuePercentage' , placeholder:"5%" },
                { label: 'Facilitator', name: '_faciliatatorRevenuePercentage' , placeholder:"10%" },
                { label: 'Project Owner', name: '_projectOwnerRevenuePercentage' , placeholder:"10%" },
                { label: 'Funders', name: '_funderRevenuePercentage' , placeholder:"75%" },
              ],
        },
        {
            name: 'Withdraw Funds',
            entrypoint: 'withdrawFunds',
            payable: false,
            fields: [
                { name: "Withdraw Funds from collectionTreasury", heading: true },
            ]
        },
        {
            name: 'Withdraw Project Owner Stake',
            entrypoint: 'withdrawProjectOwnerStake',
            payable: false,
            fields: [
                { name: "Transfer staked amount to Project Owner", heading: true },
            ]
        },
        {
            name: 'Payout',
            entrypoint: 'payout',
            payable: false,
            fields: [
                { name: "Payout to stake holders", heading: true },
            ]
        },
        {
            name: 'dissolve',
            entrypoint: 'dissolve',
            payable: false,
            fields: [
                { name: "Dissolve Protocol", heading: true },
            ]
        },
      ],
    },
    {
      name: 'Project Owner Actions',
      actions: [
        {
            name: 'Set Token Metadata URL',
            entrypoint: 'setTokenMetadataUrl',
            payable: true,
            fields: [
                { label: 'Token Metadata Url', name: '_tokenMetadataUrl' ,placeholder:"bytes of ipfs url" }
            ]
        },
        {
            name: 'stake',
            entrypoint: 'stake',
            payable: true,
            fields: [
                { label: 'Stake Amount', name: 'stake_amount' ,placeholder:"1000000" }
            ]
        },
        {
            name: 'Collect Revenue',
            entrypoint: 'collectRevenue',
            payable: true,
            fields: [
                { label: 'Add revenue', name: 'revenue_amount' ,placeholder:"1000000" }
            ]
        }

      ],
    },
    {
        name: 'Funder Actions',
        actions: [
            {
                name: 'fund',
                entrypoint: 'mint',
                payable: true,
                fields: [
                  { name: "Mint", heading: true },
                ]
            }
        ]
    }
  ];