// Dashboard.js
import React, { useState } from 'react';
import Sidebar from './Sidebar';
import Card from './Card';
import { navItems } from './navItems';
import { StorageType } from '../types/StorageType';

const Dashboard: React.FC<{contractAddress:string,contractStorage?:StorageType}> = ({
  contractAddress,
  contractStorage
}) => {
  const [activeNavItem, setActiveNavItem] = useState<string>('Contract Overview');

  const handleNavItemClick = (item: string) => {
    setActiveNavItem(item);
  };

  // const contractOverviewItem = navItems.find(item => item.name === 'Contract Overview');

  // if (contractOverviewItem) {
  //   contractOverviewItem.actions = [

  //     // Add more actions as needed
  //   ];
  // }

  return (
    <div className="container-fluid pb-4 w-80">
      <div className="row">
        <Sidebar activeNavItem={activeNavItem} onNavItemClick={handleNavItemClick} navItems={navItems} />
        <Card activeNavItem={activeNavItem} navItems={navItems} contractAddress={contractAddress} contractStorage={contractStorage}/>
      </div>
    </div>
  );
};

export default Dashboard;
