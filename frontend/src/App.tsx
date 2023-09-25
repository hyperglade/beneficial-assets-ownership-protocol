import React, { useState, useEffect } from "react";

// Components
import Navbar from "./components/Navbar";
import { fetchStorage } from "./utils/tzkt";
import { StorageType } from "./types/StorageType";
import Dashboard from "./components/Dashboard";
import ContractBar from "./components/ContractBar";

const App: React.FC = () => {
  const [address, setAddress] = useState<string>("");
  const [storage, setStorage] = useState<StorageType>();
  // Set storage 
  // KT1Cey6feQCQP2zBqhMRW24baJ9wB5YvhJ5S
  useEffect(() => {
    if (address) {
      fetchStorage(address).then((res) => setStorage(res))};
    },[address]);
  
  // console.log(storage);
  return (
    <div className="h-100">
      <Navbar />
      <ContractBar contractAddress={address} setContractAddress={setAddress} setContractStorage={setStorage}/>
      <Dashboard contractAddress={address} contractStorage={storage}/>
    </div>
  );
};

export default App;
