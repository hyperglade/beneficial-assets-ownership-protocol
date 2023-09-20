import React, { useState } from 'react';
import { StorageType } from '../types/StorageType';
import { NavItem } from '../types/navItems';
import { contractInteraction } from '../utils/operation';
import { ContractStorageType, TransactionWalletOperation } from '@taquito/taquito';



const Card: React.FC<{ activeNavItem: string; navItems: NavItem[];contractAddress : string; contractStorage?: StorageType }> = ({ activeNavItem, navItems ,contractAddress ,contractStorage }) => {
  const [formData, setFormData] = useState<{ [key: string]: string }>({});

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async(entrypoint: string) => {
    // Find the action object based on the selected entrypoint
    const selectedAction = navItems
      .flatMap((navItem) => navItem.actions)
      .find((action) => action?.entrypoint === entrypoint);
  
    if (selectedAction) {
      const fieldNames = selectedAction.fields.map((field) => field.name);
  
      // Filter the formData state to get values for the selected field names
      const selectedFieldValues: { [key: string]: string } = {};
      Object.keys(formData).forEach((fieldName) => {
        if (fieldNames.includes(fieldName)) {
          selectedFieldValues[fieldName] = formData[fieldName];
        }
      });
  
      console.log('Field Names:', fieldNames);
      console.log('Field Values:', selectedFieldValues);
      console.log('Contract Address:', contractAddress);
      
      const op = await contractInteraction(contractAddress, entrypoint, selectedFieldValues , selectedAction.payable);

      console.log("Operation Done", op)
      
    } else {
      console.error('Action not found for entrypoint:', entrypoint);
    }
  };

  function getFieldFromStorage(obj: StorageType|undefined, keys: string[]): any {
    let value: any = obj;
    if (value !== undefined){
      for (let key of keys) {
        if (value.hasOwnProperty(key)) {
          value = value[key];
        } else {
          return 'N/A'; // Field not found
        }
      }
    }
    return value;
  }
  

  const getActionForNavItem = () => {
    const navItem = navItems.find((item) => item.name === activeNavItem);
    return navItem ? navItem.actions || [] : [];
  };

  const fieldsToShow = [
    // 'token.address',
    // 'token.tokenId',
    // 'metadata',
    // 'operators',
    // 'administrator',
    // 'fundingMethod',
    // 'token_metadata',
    // 'tokenMetadataUrl',
    'protocolStatus',
    'protocolOwner',
    'facilitator',
    'projectOwner',
    'mintingPrice',
    'fundingAmount',
    'last_token_id',
    'collectedRevenue',
    'collectionTreasury',
    'distributionTreasury',
    'projectOwnerStake',
    'minRaisePercentage',
    'funderRevenuePercentage',
    'projectOwnerStakeRequirement',
    'faciliatatorRevenuePercentage',
    'projectOwnerRevenuePercentage',
    'protocolOwnerRevenuePercentage',
    // 'ledger',
  ];
  

  const renderCard = () => {
    return (
      <div className="card shadow">
        <div className="card-body">
          <h5 className="card-title">{activeNavItem}</h5>
          <form>
            {getActionForNavItem().map((action) => (
              action.name === 'contractOverview' ? (
              <>
                <p>Contract address: {contractAddress}</p>
                <dl className="row">
                {contractStorage?
                fieldsToShow.map((field, index) => {
                  const fieldKeys = field.split('.');
                  const fieldValue = getFieldFromStorage(contractStorage, fieldKeys);
                  return (
                    <React.Fragment key={index}>
                      <dt className="col-sm-6">{fieldKeys[fieldKeys.length - 1]}</dt>
                      <dd className="col-sm-6">{fieldValue}</dd>
                    </React.Fragment>
                  );
                })
                :<></>
                }
                </dl>
              </>
              ) : (
              <div key={action.name} >
                <h5 className="">{action.name}</h5>
                {action.fields.map((field) => (
                  field.heading ? (
                    <p key={field.name} className="form-group">
                      {field.name}
                    </p>
                  ) : (
                    <div className="mb-3 row" key={field.name}>
                      <label htmlFor={field.name} className="form-label col-sm-4">
                        {field.label}:
                      </label>
                      <div className="col-sm-8">
                        <input
                          type="text"
                          className="form-control"
                          id={field.name}
                          name={field.name}
                          placeholder={field.placeholder}
                          value={formData[field.name] || ''}
                          onChange={handleInputChange}
                          required={true}
                        />
                      </div>
                    </div>
                  )
                ))}
                <div className='mb-3 border-bottom' style={{height:'3rem'}}>
                  <button type='button' onClick={()=>handleSubmit(action.entrypoint)} className="btn" style={{color:'#fff',backgroundColor:'#4e4e4f',borderColor:'#4e4e4f'}}>
                    Execute
                  </button>
                </div>
              </div>
              )
            ))}
          </form>
        </div>
      </div>
    );
  };

  return (
    <main className="col-md-8 ms-sm-auto col-lg-8 px-md-4">
      <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
        <h1 className="h2">Actions</h1>
      </div>
      {renderCard()}
    </main>
  );
};

export default Card;
