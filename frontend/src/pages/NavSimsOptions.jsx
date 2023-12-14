import React, {useState} from 'react';
import { NavLink, Routes, Route } from 'react-router-dom';
const imgDir = require.context('../img/', true);
function NavSimsOptions() {
    let titleDefault = "Welcome to the simulation portal.";
    let underConstructionTitle = "Under Construction";
    let descDefault =
    "Please hover on the items on the left for a basic description. Click on them to be redirected to the relevant simulations page.";

    const [cursorLastOptionClassName, setCursorLastOptionClassName] = useState('defaultView');
    const [cursorLastOptionArrId, setCursorLastOptionArrId] = useState(0);

    const handleCursorLastOption = e => {
        setCursorLastOptionClassName(e.currentTarget.className);
        setCursorLastOptionArrId(parseInt((e.currentTarget.getAttribute('arrId'))));
        // e.currentTarget.className will return the name of the array (i.e. ADS_list)
        // parseInt((e.currentTarget.getAttribute('arrId'))) will return the number of the custom attr arrId
    };
    const handleCursorLeave = e => {
        setCursorLastOptionClassName('defaultView');
        setCursorLastOptionArrId(0)
    };

    const defaultView = [{title: titleDefault, imgId: '', desc: descDefault}];
    const ADS_list =
        [{id: 0, title: 'Electric Vehicles', imgId: '', desc: '', link: ''},
        {id: 1, title: 'Electric Bikes', imgId: '', desc: '', link: ''},
        {id: 2, title: 'Stationary Energy Storage System', imgId: '', desc: '', link: ''}];
    const BCS_list =
        [{id: 0,
            title: 'Equivalent Circuit Model',
            imgId: '',
            desc: '',
            link: '/batterysim/ecm'
        },
        {
            id: 1,
            title: 'Single Particle Model',
            imgId: 'sp.png',
            desc: 'Outputs the battery cell voltage, electrode SOC, and lumped thermal profile from parameter-set values.',
            link: '/batterysim/sp'
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

    const navListCollection = {
        defaultView,ADS_list,BCS_list,insights_list,BMSM_list
    };

    function callFunctionByName(name){
        let selectedList = navListCollection[name];
        if (selectedList) {
            return selectedList;
        } else {
            console.error(`Array ${name} not found.`);
            return {}; // return emtpy object
        }
    }


    function CreateNavList({arg_list}){
        let selectedArr = callFunctionByName(arg_list);
        return (
            selectedArr.map(selected =>
                <li className={
                    arg_list}
                    arrId={selected.id}
                    key={selected.id}
                    onMouseEnter={handleCursorLastOption}
                    onMouseLeave={handleCursorLeave}
                >
                    <NavLink to={selected.link}>
                        {selected.title}
                    </NavLink>
                </li>
            )
        )
    }

    function CreateDescription(){
        let selectedDescription = callFunctionByName(cursorLastOptionClassName);
        return (
            <React.Fragment>
                <h2>Description</h2>
                <h3 id="id_h3_description">
                    {selectedDescription[cursorLastOptionArrId].desc !== '' ? selectedDescription[cursorLastOptionArrId].title : underConstructionTitle}
                </h3>
                <p id="id_p_description">{selectedDescription[cursorLastOptionArrId].desc}</p>
                {selectedDescription[cursorLastOptionArrId].imgId !== '' ?
                    <img id="id_img" src={imgDir(`./${selectedDescription[cursorLastOptionArrId].imgId}`)} alt=""/> : null
                }
            </React.Fragment>
        );
    }

    return(
        <div>
        <nav className={"nav-sims-options"}>
            <ul className={"ul-sims-options"}>
                <li><span className="main-sim-options-span">Application Dynamics Simulation</span></li>
                <CreateNavList arg_list={"ADS_list"} />
                <li><span className="main-sim-options-span">Battery Cell Simulations</span></li>
                <CreateNavList arg_list={"BCS_list"} />
                <li><span className="main-sim-options-span">Insights</span></li>
                <CreateNavList arg_list={"insights_list"} />
                <li><span className="main-sim-options-span">Battery Management System Monitoring</span></li>
                <CreateNavList arg_list={"BMSM_list"} />
            </ul>
        </nav>
            <div className={'section-description'}>
                <CreateDescription/>
            </div>
        </div>
    );
}
export default NavSimsOptions;