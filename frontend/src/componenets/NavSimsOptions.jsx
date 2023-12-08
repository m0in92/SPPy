import React, {useState} from 'react';
import { NavLink, Routes, Route } from 'react-router-dom';
function NavSimsOptions() {
    let normalHeading = "Welcome to the simulation portal.";
    let spHeading = "Single Particle Model";
    let underConstructionHeading = "Under Construction";

    const [cursorLastOption, setCursorLastOption] = useState('')
    const handleCursorLastOption = e => {
        setCursorLastOption(e.currentTarget.textContent)
    };
    return(
        <div>
        <nav className={"nav-sims-options"}>
            <ul className={"ul-sims-options"}>
                <li><span className="main-sim-options-span">Application Dynamics Simulation</span></li>
                <li className={cursorLastOption} onMouseEnter={handleCursorLastOption}></li>
                <li className={cursorLastOption} onMouseEnter={handleCursorLastOption}></li>
                <li className={cursorLastOption} onMouseEnter={handleCursorLastOption}></li>
                <li className={cursorLastOption} onMouseEnter={handleCursorLastOption}></li>
                <li><span className="main-sim-options-span">Battery Cell Simulations</span></li>
                <li className={cursorLastOption} onMouseEnter={handleCursorLastOption}></li>
                <li className={cursorLastOption} onMouseEnter={handleCursorLastOption}></li>
                <li className={cursorLastOption} onMouseEnter={handleCursorLastOption}></li>
                <li className={cursorLastOption} onMouseEnter={handleCursorLastOption}></li>
                <li className={cursorLastOption} onMouseEnter={handleCursorLastOption}><span className="main-sim-options-span">Insights</span></li>
                <li className={cursorLastOption} onMouseEnter={handleCursorLastOption}></li>
                <li className={cursorLastOption} onMouseEnter={handleCursorLastOption}></li>
                <li><span className="main-sim-options-span">Battery Management System Monitoring</span></li>
                <li className={cursorLastOption} onMouseEnter={handleCursorLastOption}></li>
                <li className={cursorLastOption} onMouseEnter={handleCursorLastOption}></li>
                <li className={cursorLastOption} onMouseEnter={handleCursorLastOption}></li>
                <li><NavLink to='/'>Home</NavLink></li>
                <li><NavLink to='/about'>About</NavLink></li>
                <li><NavLink to='/contact'>Contact</NavLink></li>
            </ul>
        </nav>
            <div className={'section-description'}>

            </div>
        </div>
    );
}
export default NavSimsOptions;