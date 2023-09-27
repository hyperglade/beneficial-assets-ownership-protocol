import smartpy as sp

# FA2Coin = sp.io.import_stored_contract("FA2Coin")
FA2Coin = sp.io.import_script_from_url("file:FA2.py")
FA2 = sp.io.import_script_from_url("https://legacy.smartpy.io/templates/fa2_lib.py")
Utils = sp.io.import_script_from_url("https://raw.githubusercontent.com/RomarQ/tezos-sc-utils/main/smartpy/utils.py")


class BAOProtocol(FA2.Admin, 
                  FA2.MintNft, 
                  FA2.Fa2Nft):
    def __init__(self, admin, metadata, **kwargs):
        FA2.Fa2Nft.__init__(self, metadata)
        FA2.Admin.__init__(self, admin) 
        self.update_initial_storage(
            **kwargs)
        
    def TransferFATwoTokens(sender,receiver,amount,tokenAddress,id):
        """Transfers FA2 tokens 
        Args:
            sender: sender address
            receiver: receiver address
            amount: amount of tokens to be transferred
            tokenAddress: address of the FA2 contract
            id: id of token to be transferred
        """
    
        arg = [
            sp.record(
                from_ = sender,
                txs = [
                    sp.record(
                        to_         = receiver,
                        token_id    = id, 
                        amount      = amount 
                    )
                ]
            )
        ]
    
        transferHandle = sp.contract(
            sp.TList(sp.TRecord(from_=sp.TAddress, txs=sp.TList(sp.TRecord(amount=sp.TNat, to_=sp.TAddress, token_id=sp.TNat).layout(("to_", ("token_id", "amount")))))), 
            tokenAddress,
            entry_point='transfer').open_some()
    
        sp.transfer(arg, sp.mutez(0), transferHandle)


    @sp.entry_point
    def setFacilitator(self, params):
        sp.set_type(params,sp.TRecord(_facilitator = sp.TAddress))
        sp.verify(sp.sender == self.data.protocolOwner, "User is not protocolOwner")
        self.data.facilitator = sp.some(params._facilitator)

        
    @sp.entry_point
    def initProtocol(self,params):
        sp.verify(self.data.protocolStatus == "INACTIVE" , "Protocol already activated once" )
        sp.verify(sp.sender == self.data.facilitator.open_some())
        sp.set_type(params,sp.TRecord(_projectOwner = sp.TAddress , 
                                      _mintingPrice = sp.TNat, 
                                      _fundingAmount = sp.TNat, 
                                      _minRaisePercentage =sp.TNat ,
                                      _projectOwnerStakeRequirement = sp.TNat, 
                                      _projectOwnerRevenuePercentage = sp.TNat, 
                                      _faciliatatorRevenuePercentage = sp.TNat, 
                                      _funderRevenuePercentage = sp.TNat, 
                                      _protocolOwnerRevenuePercentage = sp.TNat))
        sp.verify((params._projectOwnerRevenuePercentage + params._faciliatatorRevenuePercentage + params._funderRevenuePercentage + params._protocolOwnerRevenuePercentage) == 100 , "Sum of percentages should be 100")
        self.data.projectOwner =  sp.some(params._projectOwner)
        self.data.mintingPrice =  params._mintingPrice
        self.data.fundingAmount =  params._fundingAmount
        self.data.minRaisePercentage =  params._minRaisePercentage
        self.data.projectOwnerStakeRequirement =  params._projectOwnerStakeRequirement
        self.data.projectOwnerRevenuePercentage =  params._projectOwnerRevenuePercentage
        self.data.faciliatatorRevenuePercentage =  params._faciliatatorRevenuePercentage
        self.data.funderRevenuePercentage =  params._funderRevenuePercentage
        self.data.protocolOwnerRevenuePercentage =  params._protocolOwnerRevenuePercentage

    @sp.entry_point
    def setTokenMetadataUrl(self, params):
        sp.verify(sp.sender == self.data.projectOwner.open_some(), "User is not projectOwner")
        sp.set_type(params,sp.TRecord(_tokenMetadataUrl=sp.TBytes))
        self.data.tokenMetadataUrl = params._tokenMetadataUrl

    @sp.entry_point
    def withdrawProjectOwnerStake(self):
        sp.verify(sp.sender == self.data.facilitator.open_some(), "User is not facilitator")
        BAOProtocol.TransferFATwoTokens(sp.self_address,self.data.projectOwner.open_some(),self.data.projectOwnerStake,self.data.token.address,self.data.token.tokenId)
    
    @sp.entry_point
    def stake(self, params):
        sp.set_type(params, sp.TRecord(_projectOwnerStake=sp.TNat))
        sp.verify(sp.sender == self.data.projectOwner.open_some() , "User is not projectOwner")
        sp.verify(self.data.protocolStatus == "INACTIVE" , "Protocol already activated once" )
        sp.verify(params._projectOwnerStake == self.data.projectOwnerStakeRequirement , "Amount mismatch projectOwnerStakeRequirement")
        BAOProtocol.TransferFATwoTokens(sp.sender,sp.self_address,params._projectOwnerStake,self.data.token.address,self.data.token.tokenId)
        self.data.projectOwnerStake = params._projectOwnerStake
        self.data.protocolStatus = "ACTIVE"

    @sp.entry_point
    def mint(self):
        sp.verify(self.data.fundingAmount > self.data.collectionTreasury  , "Maximum Funding Reached." )
        sp.verify(self.data.protocolStatus == "ACTIVE" , "Protocol is not active" )
        BAOProtocol.TransferFATwoTokens(sp.sender,sp.self_address,self.data.mintingPrice,self.data.token.address,self.data.token.tokenId)
        params = [
            sp.record(
                to_  = sp.sender, 
                metadata = { 
                    "" : self.data.tokenMetadataUrl
                },
            )
        ]
        self.data.collectionTreasury += self.data.mintingPrice
        sp.for action in params:
            compute_fa2_lib_601i = sp.local("compute_fa2_lib_601i", self.data.last_token_id)
            self.data.token_metadata[compute_fa2_lib_601i.value] = sp.record(token_id = compute_fa2_lib_601i.value, token_info = action.metadata)
            self.data.ledger[compute_fa2_lib_601i.value] = action.to_
            self.data.last_token_id += 1
                       
    @sp.entry_point
    def withdrawFunds(self):
        sp.verify(sp.sender == self.data.facilitator.open_some(), "User is not facilitator")
        sp.verify(self.data.protocolStatus == "ACTIVE" , "Protocol is not active" )
        fundsRequired = sp.set_type_expr(((self.data.minRaisePercentage * self.data.fundingAmount) // 100) , sp.TNat)
        sp.verify(self.data.collectionTreasury >= fundsRequired , "Insufficient funds in collectionTreasury")
        # Transfer the funds to the project owner's wallet
        BAOProtocol.TransferFATwoTokens(sp.self_address,self.data.projectOwner.open_some(),self.data.collectionTreasury,self.data.token.address,self.data.token.tokenId)
        self.data.collectionTreasury = sp.nat(0)
        self.data.protocolStatus = "FUNDED"

    @sp.entry_point
    def collectRevenue(self, params):
        sp.set_type(params, sp.TRecord(_collectRevenue=sp.TNat))
        sp.verify(sp.sender == self.data.projectOwner.open_some() ,"User is not projectOwner")
        sp.verify(self.data.protocolStatus == "FUNDED" ,"Protocol not FUNDED")
    
        BAOProtocol.TransferFATwoTokens(sp.sender,sp.self_address,params._collectRevenue,self.data.token.address,self.data.token.tokenId)
        self.data.distributionTreasury += params._collectRevenue

    
    @sp.entry_point
    def payout(self):
        sp.verify(sp.sender == self.data.facilitator.open_some(), "User is not facilitator")
        sp.verify(self.data.distributionTreasury > 0, "Empty distributionTreasury")
        projectOwnerShare = ((self.data.projectOwnerRevenuePercentage * self.data.distributionTreasury) //100 ) 
        facilitatorShare = ((self.data.faciliatatorRevenuePercentage * self.data.distributionTreasury) //100 ) 
        protocolOwnerShare = ((self.data.protocolOwnerRevenuePercentage * self.data.distributionTreasury) //100 ) 
        funderShare = ((self.data.funderRevenuePercentage * self.data.distributionTreasury) //100 ) //sp.len(self.data.ledger) 
        total = projectOwnerShare + facilitatorShare + protocolOwnerShare + (funderShare * sp.len(self.data.ledger))
        sp.if total == self.data.distributionTreasury:
            BAOProtocol.TransferFATwoTokens(
                sp.self_address,
                self.data.projectOwner.open_some(),
                projectOwnerShare,
                self.data.token.address,
                self.data.token.tokenId)
            
            BAOProtocol.TransferFATwoTokens(
                sp.self_address,
                self.data.facilitator.open_some(),
                facilitatorShare,
                self.data.token.address,
                self.data.token.tokenId)
            
            BAOProtocol.TransferFATwoTokens(
                sp.self_address,
                self.data.protocolOwner,
                protocolOwnerShare,
                self.data.token.address,
                self.data.token.tokenId)
    
            funders = self.data.ledger.values()
            sp.for funder in funders:
                BAOProtocol.TransferFATwoTokens(
                    sp.self_address,
                    funder,
                    funderShare,
                    self.data.token.address,
                    self.data.token.tokenId)
        
            self.data.distributionTreasury = sp.nat(0)

    @sp.entry_point
    def dissolve(self):
        sp.verify(sp.sender == self.data.facilitator.open_some(), "User is not facilitator")
        sp.verify(self.data.protocolStatus == "ACTIVE", "Protocol is not active")

        funders = self.data.ledger.values()
        sp.for funder in funders:
            BAOProtocol.TransferFATwoTokens(
                sp.self_address,
                funder,
                self.data.mintingPrice,
                self.data.token.address,
                self.data.token.tokenId)
        
        BAOProtocol.TransferFATwoTokens(
            sp.self_address,
            self.data.projectOwner.open_some(),
            self.data.projectOwnerStakeRequirement,
            self.data.token.address,
            self.data.token.tokenId)
        
        self.data.protocolStatus = "DISOLVED" 
        
        
        
@sp.add_test(name="BAOProtocol Init")
def test():
    admin = sp.test_account("admin")
    facil = sp.test_account("facil")
    alice = sp.test_account("alice")
    bob = sp.test_account("bob")

    coin = FA2Coin.FA2(
            FA2Coin.FA2_config(),
            sp.utils.metadata_of_url("https://example.com"),
            admin.address,
        )
    
    scenario = sp.test_scenario()
    
    scenario.h2("USDT token copy (FA2) for testing")
    scenario += coin
    
    
    BAO = BAOProtocol(
        admin = admin.address,
        metadata = sp.utils.metadata_of_url("ipfs://bafkreidxv6n6fk5m45eytksqs3iests45hqvz7k5ck2fos6cyelt3viea4"),
        ledger = {},
        token = sp.record(address=coin.address,tokenId=sp.nat(0)),
        tokenMetadataUrl = sp.bytes("0x697066733a2f2f6261666b726569647876366e36666b356d34356579746b73717333696573747334356871767a376b35636b32666f73366379656c74337669656134"),
        protocolStatus = "INACTIVE",
        protocolOwner = admin.address,
        facilitator = sp.none,
        projectOwner = sp.none,
        mintingPrice = sp.nat(0),
        fundingAmount = sp.nat(0),
        fundingMethod = "NFT_MINT",
        collectionTreasury = sp.nat(0),
        distributionTreasury = sp.nat(0),
        collectedRevenue = sp.nat(0),
        projectOwnerStake = sp.nat(0),
        minRaisePercentage = sp.nat(0),
        projectOwnerStakeRequirement = sp.nat(0),
        projectOwnerRevenuePercentage = sp.nat(0),
        faciliatatorRevenuePercentage = sp.nat(0),
        funderRevenuePercentage = sp.nat(0),
        protocolOwnerRevenuePercentage = sp.nat(0)
    )
    scenario.h1("BA0Protocol contract")
    scenario += BAO
    
    scenario.h1("Setting Facilitator")
    scenario += BAO.setFacilitator(_facilitator=facil.address).run(sender = admin.address)
    
    scenario.h1("Calling init by Facilitator")
    initParams = sp.record(
        _projectOwner = admin.address , 
        _mintingPrice = sp.nat(1000000), 
        _fundingAmount = sp.nat(4000000), 
        _minRaisePercentage = sp.nat(50) ,
        _projectOwnerStakeRequirement = sp.nat(1000000), 
        _projectOwnerRevenuePercentage = sp.nat(20), 
        _faciliatatorRevenuePercentage = sp.nat(20), 
        _funderRevenuePercentage = sp.nat(50), 
        _protocolOwnerRevenuePercentage = sp.nat(10))
    scenario += BAO.initProtocol(initParams).run(sender = facil)

    scenario += BAO.setTokenMetadataUrl(
        _tokenMetadataUrl = sp.bytes("0x697066733a2f2f6261666b726569647876366e36666b356d34356579746b73717333696573747334356871767a376b35636b32666f73366379656c74337669656134")
    ).run(sender=admin.address)
    
    coin.mint(
            address=admin.address,
            amount=2000000,
            metadata=FA2Coin.FA2.make_metadata(name="TOKEN", decimals=6, symbol="TKN"),
            token_id=0,
        ).run(sender=admin)
    
    coin.mint(
            address=alice.address,
            amount=2000000,
            metadata=FA2Coin.FA2.make_metadata(name="TOKEN", decimals=6, symbol="TKN"),
            token_id=0,
        ).run(sender=admin)
    
    coin.mint(
            address=bob.address,
            amount=1000000,
            metadata=FA2Coin.FA2.make_metadata(name="TOKEN", decimals=6, symbol="TKN"),
            token_id=0,
        ).run(sender=admin)
    
    coin.update_operators(
            [sp.variant("add_operator", sp.record(owner=admin.address, operator=BAO.address, token_id=0))]
        ).run(sender=admin)
    
    coin.update_operators(
            [sp.variant("add_operator", sp.record(owner=alice.address, operator=BAO.address, token_id=0))]
        ).run(sender=alice)
    
    coin.update_operators(
            [sp.variant("add_operator", sp.record(owner=bob.address, operator=BAO.address, token_id=0))]
        ).run(sender=bob)
    
    scenario.h1("Stake")
    scenario.p("Staking by Project Owner")
    scenario += BAO.stake(
        _projectOwnerStake=sp.nat(1000000)
    ).run(sender = admin ,valid=True)
    scenario.p("Staking by any other")
    scenario += BAO.stake(
        _projectOwnerStake=sp.nat(1000000)
    ).run(sender = bob, valid=False)
    
    NFT = FA2.make_metadata(
        name     = "Example FA2",
        decimals = 6,
        symbol   = "EFA2" )

    mint_params = sp.record(
        amount = sp.nat(1000000), 
        _params = [
            sp.record(
                to_  = alice.address, 
                metadata = NFT
            )
        ]
    )
    
    scenario.h1("Mint")
    scenario.p("Minting for Alice")
    scenario += BAO.mint().run(sender=alice)
    scenario.p("Minting for Bob")
    scenario += BAO.mint().run(sender=bob)


    scenario.h1("WithdrawFunds")
    scenario += BAO.withdrawFunds().run(sender=facil)
    scenario += BAO.withdrawFunds().run(sender=bob,valid=False)
    
    scenario.h1("Collect Revenue")
    scenario += BAO.collectRevenue(
        _collectRevenue=1000000
    ).run(sender=admin)

    scenario.h1("Withdraw Project Owner Stake")
    scenario += BAO.withdrawProjectOwnerStake().run(sender=facil)

    scenario.h1("Payout")
    scenario += BAO.payout().run(sender=bob,valid=False)
    scenario += BAO.payout().run(sender=facil)

    scenario.h1("Dissolve")
    scenario += BAO.dissolve().run(sender=facil,valid=False)

