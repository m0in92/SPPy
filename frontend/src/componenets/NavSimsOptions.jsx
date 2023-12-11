import React, {useState} from 'react';
import { NavLink, Routes, Route } from 'react-router-dom';
function NavSimsOptions() {
    let titleDefault = "Welcome to the simulation portal.";
    let underConstructionTitle = "Under Construction";
    let welcomeDesc =
    "Please hover on the items on the left for a basic description. Click on them to be redirected to the relevant simulations page.";

    const imgDir = '../img/'

    const [cursorLastOptionTitle, setCursorLastOptionTitle] = useState(titleDefault);
    const [cursorLastOptionDesc, setCursorLastOptionDesc] = useState(welcomeDesc);
    const [cursorLastOptionImgId, setCursorLastOptionImgId] = useState('');

    const handleCursorLastOption = e => {
        setCursorLastOptionTitle(e.currentTarget.textContent);
        // e.currentTarget.className will return the name of the array (i.e. ADS_list)
        // parseInt((e.currentTarget.getAttribute('arrId'))) will return the number of the custom attr arrId
        setCursorLastOptionDesc(e.currentTarget.className[parseInt((e.currentTarget.getAttribute('arrId')))].desc);
        setCursorLastOptionImgId(e.currentTarget.className[parseInt((e.currentTarget.getAttribute('arrId')))].imgId);
    };
    const handleCursorLeave = e => {
        setCursorLastOptionTitle(titleDefault);
        setCursorLastOptionDesc(welcomeDesc);
        setCursorLastOptionImgId('');
    };

    const ADS_list =
        [{id: 0, title: 'Electric Vehicles', imgId: '', desc: '', link: ''},
        {id: 1, title: 'Electric Bikes', imgId: '', desc: '', link: ''},
        {id: 2, title: 'Stationary Energy Storage System', imgId: '', desc: '', link: ''}];
    const BCS_list =
        [{id: 0, title: 'Equivalent Circuit Model', imgId: '', desc: '', link: ''},
        {
            id: 1,
            title: 'Single Particle Model',
            imgId: 'sp.png',
            desc: 'Outputs the battery cell voltage, electrode SOC, and lumped thermal profile from parameter-set values.',
            link: ''
        },
        {id: 2, title: 'Enhanced Single Particle Model', imgId: '', desc: '', link: ''},
        {id: 3, title: 'Pseudo Two Dimensional Model', imgId: '', desc: '', link: ''}];
    const insights_list =
        [{id: 0, title: 'Range Estimations', imgId: '', desc: '', link: ''},
        {id: 1, title: 'Life Cycle Estimations', imgId: '', desc: '', link: ''}];
    const BMSM_list =
        [{id: 0, title: 'SOC Estimations with Kalman Filter', imgId: '', desc: '', link: ''},
        {id: 1, title: 'SOH Estimations with Kalman Filter', imgId: '', desc: '', link: ''},
        {id: 2, title: 'Potential Fault Detection', imgId: '', desc: '', link: ''}];

    function CreateNavList({arg_list}){
        return (
            arg_list.map(arg =>
                <li className={
                    Object.keys({arg_list})[0]}
                    arrId={arg.id}
                    key={arg.id}
                    onMouseEnter={handleCursorLastOption}
                    onMouseLeave={handleCursorLeave}
                >
                    <NavLink to={arg.link}>
                        {arg.title}
                    </NavLink>
                </li>
            )
        )
    }

    function CreateDescription(){
        return (
            <React.Fragment>
                <h2>Description</h2>
                <h3 id="id_h3_description">
                    {cursorLastOptionDesc !== '' ? cursorLastOptionTitle : underConstructionTitle}
                </h3>
                <p id="id_p_description">{cursorLastOptionDesc}</p>
                {cursorLastOptionImgId !== '' ?
                    <img id="id_img" src={imgDir + cursorLastOptionImgId} alt=""/> : null
                }
            </React.Fragment>
        );
    }

    return(
        <div>
        <nav className={"nav-sims-options"}>
            <ul className={"ul-sims-options"}>
                <li><span className="main-sim-options-span">Application Dynamics Simulation</span></li>
                <CreateNavList arg_list={ADS_list} />
                <li><span className="main-sim-options-span">Battery Cell Simulations</span></li>
                <CreateNavList arg_list={BCS_list} />
                <li><span className="main-sim-options-span">Insights</span></li>
                <CreateNavList arg_list={insights_list} />
                <li><span className="main-sim-options-span">Battery Management System Monitoring</span></li>
                <CreateNavList arg_list={BMSM_list} />
            </ul>
        </nav>
            <div className={'section-description'}>
                <CreateDescription/>
            </div>
        </div>
    );
}
export default NavSimsOptions;