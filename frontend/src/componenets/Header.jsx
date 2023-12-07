import React from 'react';
 import { Link } from "react-router-dom";

function Header() {
    return (
        <div className={"header"}>
            <div className={"left_logo"}>
            <Link to={{pathname: ''}}>
                <h2 className="logo">
                    <span className="logo-span">
                        BMS
                    </span>
                    Sim
                </h2>
            </Link>
            </div>
            <div className="menu">
                <ul className="menu-list">
                    <li className="link-list">
                    <Link to={{pathname: ''}}>
                        <span className="menu-texts-span">Home</span>
                    </Link>
                    </li>
                    <li className="link-list">
                    <Link to={{pathname: ''}}>
                        <span className="menu-texts-span">About</span>
                    </Link>
                    </li>
                </ul>
            </div>

        </div>
  );
}
export default Header;