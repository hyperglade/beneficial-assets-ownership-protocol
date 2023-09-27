export interface Field {
    label?: string;
    name: string;
    placeholder?: string;
    heading?: boolean;
  }
  
export interface Action {
    name: string;
    fields: Field[];
    label?: string;
    entrypoint: string;
    payable: boolean;
  }
  
export interface NavItem {
    name: string;
    fields?: Field[];
    actions?: Action[];
  }