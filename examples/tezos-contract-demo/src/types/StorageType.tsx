export interface StorageType {
    token: {
      address: string;
      tokenId: string;
    };
    ledger: Record<string, string>;
    metadata: number;
    operators: number;
    facilitator: string;
    projectOwner: string;
    administrator: string;
    fundingAmount: string;
    fundingMethod: string;
    last_token_id: string;
    protocolOwner: string;
    protocolStatus: string;
    token_metadata: number;
    collectedRevenue: string;
    projectOwnerStake: string;
    collectionTreasury: string;
    minRaisePercentage: string;
    distributionTreasury: string;
    funderRevenuePercentage: string;
    projectOwnerStakeRequirement: string;
    faciliatatorRevenuePercentage: string;
    projectOwnerRevenuePercentage: string;
    protocolOwnerRevenuePercentage: string;
  }
  