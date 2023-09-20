// Sidebar.js
import React from 'react';

const Sidebar: React.FC<{ activeNavItem: string; onNavItemClick: (item: string) => void; navItems: { name: string }[] }> = ({
  activeNavItem,
  onNavItemClick,
  navItems,
}) => {
  return (
    <div className="col-md-4 d-none d-md-block px-md-4">
      <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
       <h1 className="h2">
            BAO Protocol
        </h1>
      </div>
      <div className="card sidebar-card shadow">
        <div className="card-body">
          <ul className="nav flex-column">
            {navItems.map((item) => (
              <li className="nav-item mb-2" key={item.name}>
                <button
                  className={`nav-link btn ${activeNavItem === item.name ? 'active' : ''}`}
                  style={{ textAlign: 'left', width: '100%',color: '#212529', backgroundColor: '#e9ecef' }}
                  onClick={() => onNavItemClick(item.name)}
                >
                  {item.name}
                </button>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
