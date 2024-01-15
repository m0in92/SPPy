import React, {useEffect, useLayoutEffect, useRef, useState} from 'react';
import axios from 'axios';
import {API_BASE_URL} from "../constants/constants";
import RenderDataPoints from "../componenets/battery_cell_simualtions/RenderDataPoints";

function Ecm(){
    const [paramNameList, setParamNameList] = useState([]);
    const [cyclerList, setCyclerList] = useState([]);
    const [socLibInit, setSocLibInit] = useState(0.0);
    const [tempInit, setTempInit] = useState(298.0);

    const [paramName, setParamName] = useState("test");
    const [cycler, setCycler] = useState("discharge");
    const [simParams, setSimParams] = useState({});


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

    return(
        <div>
            <div className="container">

            </div>
        </div>
    );
}

export default Ecm;