
import {tezos} from "./tezos"
import { getAccount } from "./wallet";

export const contractInteraction = async (
    contractAddress: string,
    entrypoint: string,
    params : any,
    payable: boolean = false,
) => {
    try{
        if (!payable) {
            const contract = await tezos.wallet.at(contractAddress);
            console.log(contract);
            if (Object.keys(params).length === 1) {
                const op = await contract.methodsObject[entrypoint](...Object.values(params)).send();
                await op.confirmation(1);
                return op.opHash;
            } else {
                const op = await contract.methodsObject[entrypoint](params).send();
                await op.confirmation(1);
                return op.opHash;
            }     
        } else {
            const contract = await tezos.wallet.at(contractAddress);
            const USDtContract = await tezos.wallet.at("KT1WNrZ7pEbpmYBGPib1e7UVCeC6GA6TkJYR");
            const userAddress = await getAccount();
            const batchOp = await tezos.wallet.batch()
            .withContractCall(USDtContract.methods.update_operators([
                {
                    add_operator: {
                        owner: userAddress,
                        operator: contractAddress,
                        token_id: 0
                    }
                }
            ]))
            .withContractCall(contract.methodsObject[entrypoint](...Object.values(params)))
            .send();
            await batchOp.confirmation(1);   
            return batchOp.opHash;
        }
    }
    catch(err){
        throw err;
    }
};
