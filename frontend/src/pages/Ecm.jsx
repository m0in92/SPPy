import React, {useEffect, useLayoutEffect, useRef, useState} from 'react';
import axios from 'axios';
import {API_BASE_URL} from "../constants/constants";
import RenderDataPoints from "../componenets/battery_cell_simualtions/RenderDataPoints";
import '../css/Ecm.css';

function Ecm(){
    const [paramNameList, setParamNameList] = useState([]);
    const [cyclerList, setCyclerList] = useState([]);
    const [socLibInit, setSocLibInit] = useState(0.0);
    const [tempInit, setTempInit] = useState(298.0);

    const [socValidity, setSocValidity] = useState(true)
    const [tempValidity, setTempValidity] = useState(true)

    const [paramName, setParamName] = useState("test");
    const [cycler, setCycler] = useState("discharge");
    const [simParams, setSimParams] = useState({});

    const [socLibSim, setSocLibSim] = useState([]);
    const [tSim, setTSim] = useState([]);
    const [tempSim, setTempSim] = useState([]);
    const [vSim, setVSim] = useState([]);


     useEffect(() => {
        axios.options(`${API_BASE_URL}/batterysim/ecm`)
            .then((rspn) => {
                setParamNameList(rspn.data["ecm_options"]["parameter_name_list"]);
                setCyclerList(rspn.data["ecm_options"]["cycler_list"]);
                setSocLibInit(rspn.data["ecm_options"]["soc_lib_init"]);
                setTempInit(rspn.data["ecm_options"]["temp_amb"]);
                //setParamName(rspn.data["ecm_options"]["parameter_name_list"][0]);
                //setCycler(rspn.data["ecm_options"]["cycler_list"][0]);
            })
            .catch((err) => {
                console.error(err);
            });
    }, []);

    useEffect(() => {
        axios.get(`${API_BASE_URL}/batterysim/ecm`, { params: {'parameter_name': paramName}})
            .then((rspn) => {
                setSimParams(JSON.parse(rspn.data["parameter_values"]));
            }).catch((err) => {
                console.error(err);
      });
    }, [paramName]);

    const baseVerifyFloatInput = (num) => {
        if (isNaN(num)) {
            return false;
        } else {
            // number must be non-negative at most 4 sigfigs
            // KNOWN BUG: adding dash in between digits or inputting 2 dashes circumvents the check
            return num.match(/^\d*(\.\d{0,4})?$/);
        }
    }

    const verifySOC = (e) => {
        let nmbr = e.target.value.trim();
        if (baseVerifyFloatInput(nmbr) && Number(nmbr) <= 1.0) {
            setSocValidity(true);
            setSocLibInit(Number(nmbr));
        } else {
            setSocValidity(false);
        }
    }

    const verifyTemp = (e) => {
        let nmbr = e.target.value.trim();
        setTempValidity(baseVerifyFloatInput(nmbr));
        if (baseVerifyFloatInput(nmbr)) {
            setTempInit(Number(nmbr))
        }
    }

    const renderedParamNameList = paramNameList.map(item => <option key={item} value={item}>{item}</option>);
    const renderedCyclerList = cyclerList.map(item => <option key={item} value={item}>{item}</option>);

    function HandleSubmit(e) {
        e.preventDefault();
        if (socValidity && tempValidity) {
            let formData = new FormData();
            formData.append("parameter_name", paramName);
            formData.append("cycler", cycler);
            formData.append("soc_lib_init", socLibInit);
            formData.append("temp_amb", tempInit);
            axios.post(`${API_BASE_URL}/batterysim/ecm`, formData)
                .then((rspn) => {
                    setSocLibSim(JSON.parse(rspn.data["soc_lib"]));
                    setTSim(JSON.parse(rspn.data["t_sim"]));
                    setTempSim(JSON.parse(rspn.data["temp_sim"]));
                    setVSim(JSON.parse(rspn.data["v_sim"]));
                })
                .catch((err) => {
                console.error(err);
            });
        }
    }
    return(
        <div>
            <div className="container">
                <form method="post" onSubmit={HandleSubmit}>
                    {/* see how forms are done: https://react.dev/reference/react-dom/components/select#reading-the-select-box-value-when-submitting-a-form
                         */}
                    <table>
                    <tbody>
                        <tr>
                            <td>Parameter Name:</td>
                            <td>
                                <label>
                                    <select value={paramName}
                                        onChange={e => setParamName(e.target.value)}>
                                        {renderedParamNameList}
                                    </select>
                                </label>
                            </td>
                        </tr>
                        <tr>
                            <td>Cycler:</td>
                            <td>
                                <label>
                                    <select value={cycler}
                                        onChange={e => setCycler(e.target.value)}>
                                        {renderedCyclerList}
                                    </select>
                                </label>
                            </td>
                        </tr>
                        <tr>
                            <td>Initial LIB SOC:</td>
                            <td>
                                <label>
                                    <input type="number"
                                           min="0.0000"
                                           max="1.0000"
                                           step="0.0001"
                                           defaultValue={0.0}
                                           inputMode="numeric"
                                           required={true}
                                           onChange={e => verifySOC(e)}/>
                                </label>
                                {(!socValidity) && <span className='input_error_warning'>&nbsp;&nbsp;Input must be a number between 0.0 and 1.0&nbsp;&nbsp;</span>}
                            </td>
                        </tr>
                        <tr>
                            <td>Ambient Temperature [K]:</td>
                            <td>
                                <label>
                                    <input type="number"
                                           min="0.0000"
                                           step="0.0001"
                                           defaultValue={298.0}
                                           inputMode="numeric"
                                           required={true}
                                           onChange={e => verifyTemp(e)}/>
                                </label>
                                {(!tempValidity) && <span className='input_error_warning'>&nbsp;&nbsp;Input must be a number greater than 0.0&nbsp;&nbsp;</span>}
                            </td>
                        </tr>
                    </tbody>
                    </table>
                    <button type="submit">Submit</button>
                </form>
                <table className="table_parameter_values">
                    <tbody>
                    <tr>
                        <th>Parameter Name</th>
                        <th>Parameter Value</th>
                    </tr>
                    <tr>
                        <th >Reference R0</th>
                        <th>{Number(simParams["R0 ref_bc [ohm]"]).toString()}</th>
                    </tr>
                    <tr>
                        <th >Reference R1</th>
                        <th>{Number(simParams["R1_ref_bc [ohm]"]).toString()}</th>
                    </tr>
                    <tr>
                        <th >C1 [F]</th>
                        <th>{Number(simParams["C1_bc [F]"]).toString()}</th>
                    </tr>
                    <tr>
                        <th >Reference Temperature [K]</th>
                        <th>{Number(simParams["temp_ref_bc [K]"]).toString()}</th>
                    </tr>
                    <tr>
                        <th>R0 Activation Energy [J/mol]</th>
                        <th>{Number(simParams["Ea_R0_bc [J/mol]"]).toString()}</th>
                    </tr>
                    <tr>
                        <th>R1 Activation Energy [J/mol]</th>
                        <th>{Number(simParams["Ea_R1_bc [J/mol]"]).toString()}</th>
                    </tr>
                    <tr>
                        <th>Instantaneous hysteresis co-efficient [V]</th>
                        <th>{Number(simParams["M_bc [V]"]).toString()}</th>
                    </tr>
                    <tr>
                        {/*not sure if data matches title*/}
                        <th>SOC-dependent hysteresis co-efficient [V]</th>
                        <th>{Number(simParams["M_0_bc [V]"]).toString()}</th>
                    </tr>
                    <tr>
                        {/*not sure if data matches title*/}
                        <th>Hysteresis time-constant</th>
                        <th>{Number(simParams["gamma_bc"]).toString()}</th>
                    </tr>
                    <tr>
                        <th>Density [<em>kg m<sup>-3</sup></em>]</th>
                        <th>{Number(simParams["rho_bc [kg/m3]"]).toString()}</th>
                    </tr>
                    <tr>
                        <th>Volume [<em>m<sup>3</sup></em>]</th>
                        <th>{Number(simParams["vol_bc [m3]"]).toString()}</th>
                    </tr>
                    <tr>
                        <th>Specific Heat [<em>J K<sup>-1</sup> kg<sup>-1</sup></em>]</th>
                        <th>{Number(simParams["C_p_bc [J/(Kkg)]"]).toString()}</th>
                    </tr>
                    <tr>
                        <th>Heat Transfer Coefficient [<em>J K<sup>-1</sup> s<sup>-1</sup></em>]</th>
                        <th>{Number(simParams["h_bc [J/(SK)]"]).toString()}</th>
                    </tr>
                    <tr>
                        {/*not sure if data matches title*/}
                        <th>Surface Area [<em>m<sup>2</sup></em>]</th>
                        <th>{Number(simParams["area_bc [m2]"]).toString()}</th>
                    </tr>
                    <tr>
                        <th>Capacity [<em>A hr</em>]</th>
                        <th>{Number(simParams["cap_bc [Ahr]"]).toString()}</th>
                    </tr>
                    <tr>
                        <th>Maximum Potential Cut-off [<em>V</em>]</th>
                        <th>{Number(simParams["V_max_bc [V]"]).toString()}</th>
                    </tr>
                    <tr>
                        <th>Minimum Potential Cut-off [<em>V</em>]</th>
                        <th>{Number(simParams["V_min_bc [V]"]).toString()}</th>
                    </tr>
                    </tbody>

                </table>

            </div>
            <div>
                {RenderDataPoints({"Time [s]": tSim}, {"SOC LIB": socLibSim})}
                {RenderDataPoints({"Time [s]": tSim}, {"Potential [V]": vSim})}
                {RenderDataPoints({"Time [s]": tSim}, {"Temperature [C]": tempSim})}
            </div>
        </div>
    );
}

export default Ecm;