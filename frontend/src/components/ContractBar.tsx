import React from 'react'
import { fetchStorage } from '../utils/tzkt';
import { StorageType } from '../types/StorageType';

const ContractBar: React.FC<{ 
    contractAddress: string; 
    setContractAddress: React.Dispatch<React.SetStateAction<string>>; 
    setContractStorage: React.Dispatch<React.SetStateAction<StorageType|undefined>>
  }> = (
    {contractAddress ,
    setContractAddress,
    setContractStorage}
  ) => {

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const inputAddress = event.target.value;
    setContractAddress(inputAddress);
  }
  const handelSubmit = () => {
    fetchStorage(contractAddress).then((res) => setContractStorage(res))
  };
  
  
  return (
    <div className="container-fluid py-4 ">
        <div className="row offset-md-4">
        <div className="input-group rounded px-md-4">
        <span className="mx-2 my-auto"> Contract Address :  </span>
            <input type="search" className="form-control rounded" placeholder="KT1..." aria-label="Search" aria-describedby="search-addon" value={contractAddress} onChange={handleInputChange} />
            <button onClick={handelSubmit} className="input-group-text border-0" id="search-addon">
              Submit
            </button>
        </div>
        </div>
    </div>
  )
}

export default ContractBar