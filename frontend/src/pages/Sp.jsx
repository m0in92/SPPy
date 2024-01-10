import React, {useEffect, useLayoutEffect, useRef, useState} from 'react';
import axios from 'axios';
import {API_BASE_URL} from "../constants/constants";
import RenderDataPoints from "../componenets/battery_cell_simualtions/RenderDataPoints";

function Sp(){
    const [paramNameList, setParamNameList] = useState([]);
    const [cyclerList, setCyclerList] = useState([]);
    const [socLibInit, setSocLibInit] = useState(0.0);

    const [paramName, setParamName] = useState("Calce_NMC_18650");
    const [cycler, setCycler] = useState('discharge');
    const [simParams, setSimParams] = useState({});

    const [socValidity, setSocValidity] = useState(true)

    const [socNSim, setSocNSim] = useState([]);
    const [socPSim, setSocPSim] = useState([]);
    const [tSim, setTSim] = useState([]);
    const [tempSim, setTempSim] = useState([]);
    const [vSim, setVSim] = useState([]);

    useEffect(() => {
        axios.options(`${API_BASE_URL}/batterysim/sp`)
            .then((rspn) => {
                setParamNameList(rspn.data["sp_options"]["parameter_name_list"]);
                setCyclerList(rspn.data["sp_options"]["cycler_list"]);
                setSocLibInit(rspn.data["sp_options"]["soc_lib_init"]);
                // setParamName(rspn.data["sp_options"]["parameter_name_list"][0]);
                // setCycler(rspn.data["sp_options"]["cycler_list"][0]);
            })
            .catch((err) => {
                console.error(err);
            });
    }, []);

    // GET the sim variables based on the parameter name. Updates everytime the user switches the param name
    useEffect(() => {
        axios.get(`${API_BASE_URL}/batterysim/sp`, { params: {'parameter_name': paramName}})
            .then((rspn) => {
                setSimParams(JSON.parse(rspn.data["parameter_values"]));
            }).catch((err) => {
                console.error(err);
      });
    }, [paramName]);

    /*const usePlotUpdater = () => {
        const didMount = useRef(false);
        useEffect(() => {
            if (didMount.current) {
                let dataPoints =
                    {"x_val" : {"Time [s]": tSim}, "y_val" :
                        {"SOC_n": socNSim,
                        "SOC_p": socPSim,
                        "Temperature [C]": tSim,
                        "Potential [V]" : vSim}
                    };
                for (let y_element in dataPoints["y_val"]){
                    for (let x_element in dataPoints["x_val"]){
                        RenderDataPoints(x_element, y_element);
                    }
                }
            } else didMount.current = true;
        }, [socNSim, socPSim, tSim, tempSim, vSim]);
    }*/


    //console.log(paramNameList)

    function HandleSubmit(e){
        e.preventDefault() // stops browser from reloading the page
        if (socValidity === true) {
            let formData = new FormData();
            formData.append("parameter_name", paramName);
            formData.append("cycler", cycler);
            formData.append("soc_lib_init", socLibInit);
            axios.post(`${API_BASE_URL}/batterysim/sp`, formData)
                .then((rspn) => {
                    console.log(rspn.data);
                    setSocNSim(JSON.parse(rspn.data["soc_n_sim"]));
                    setSocPSim(JSON.parse(rspn.data["soc_p_sim"]));
                    setTSim(JSON.parse(rspn.data["t_sim"]));
                    setTempSim(JSON.parse(rspn.data["temp_sim"]));
                    setVSim(JSON.parse(rspn.data["v_sim"]));
                })
                .catch((err) => {
                console.error(err);
            });
        }
    }

    const renderedParamNameList = paramNameList.map(item => <option key={item} value={item}>{item}</option>);
    const renderedCyclerList = cyclerList.map(item => <option key={item} value={item}>{item}</option>);

    const verifySOC = (e) => {
        console.log(paramNameList)
        // There's a concern that if the input isn't a number the number range check will crash
        // Ugly, potential room for improvement
        if (isNaN(e.target.valueAsNumber)){
            setSocValidity(false);
        } else if (e.target.valueAsNumber > 1.0 || !(e.target.value.match(/^[0-1](\.\d{0,4})?$/))){
            // number must be at most 4 sigfigs
            setSocValidity(false);
        } else {
            setSocValidity(true);
            setSocLibInit(e.target.valueAsNumber)
        }
    }
    return(
        <div>
            <div className="container">
            I H8 REACT!!1!
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
                        {(!socValidity) && <span>Input must be a number between 0.0 and 1.0</span>}

                        <div>{socValidity.toString()}</div>
                        <div>{socLibInit}</div>
                    </td>
                </tr>
                </tbody>
                </table>
                <button type="submit">Submit</button>
            </form>


            </div>
            <div>
                {RenderDataPoints({"Time [s]": tSim}, {"SOC_n": socNSim})}
            </div>
        </div>


    );
}

export default Sp;