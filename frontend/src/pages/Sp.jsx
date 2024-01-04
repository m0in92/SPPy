import React, {useEffect, useState} from 'react';
import axios from 'axios';
import {API_BASE_URL} from "../constants/constants";

function Sp(){
    const [paramName, setParamName] = useState('Chen_2020');
    const [socLibInit, setSocLibInit] = useState(0);
    const [cycler, setCycler] = useState('discharge');
    const [simParams, setSimParams] = useState({});

    useEffect(() => {
        axios.get(`${API_BASE_URL}/batterysim/sp`, { params: {'parameter_name': paramName}})
            .then( (rspn) => {
                setSocLibInit(rspn.data["soc_lib_init"]);
                setCycler(rspn.data["cycler"]);
                setSimParams(JSON.parse(rspn.data["parameter_values"]));
        }).catch(err => { });
    }, [paramName]);

    console.log(simParams)


    return(
        <div>
            I H8 REACT!!1!
            {/*VIEW_CONTEXT*/}

        </div>
    );
}

export default Sp;