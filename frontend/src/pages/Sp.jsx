import {lazy, useEffect, useState, Suspense} from 'react';
import axios from 'axios';
import {API_BASE_URL} from "../constants/constants";
import '../css/Sp.css';

//import RenderDataPoints from "../componenets/battery_cell_simualtions/RenderDataPoints";
const RenderDataPoints = lazy(() => import("../componenets/battery_cell_simualtions/RenderDataPoints"));


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
        // There's a concern that if the input isn't a number the number range check will crash
        let nmbr = e.target.value.trim();
        // Ugly, potential room for improvement
        if (Number(nmbr) <= 1.0 && !!(nmbr.match(/^[0-1](\.\d{0,4})?$/))){
            setSocValidity(true);
            setSocLibInit(e.target.valueAsNumber);
        } else {
            setSocValidity(false);
        }
    }
    return(
        <div className="sim_parent">
            <div className="container">
                <form method="post" onSubmit={HandleSubmit}>
                    {/* see how forms are done: https://react.dev/reference/react-dom/components/select#reading-the-select-box-value-when-submitting-a-form
                         */}
                    <table>
                    <tbody>
                        <tr>
                            <td className="parameter_names">Parameter Name:</td>
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
                            <td className="parameter_names">Cycler:</td>
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
                            <td className="parameter_names">Initial LIB SOC:</td>
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
                                {(!socValidity) && <span className='input_error_warning'>&nbsp;&nbsp;Input must be at most 4 decimal places between 0.0 and 1.0. &nbsp;&nbsp;</span>}
                            </td>
                        </tr>
                    </tbody>
                    </table>
                    <button type="submit">Submit</button>
                </form>
                <table className="table_parameter_values">
                    <tbody>
                    {/*<tr>
                        <th colSpan="4"><h3 className="table_main_heading" id="table_parameter_values_main_heading"></h3></th>
                    </tr>*/}

                    <tr>
                        <th></th>
                        <th>Negative Electrode</th>
                        <th>Seperator</th>
                        <th>Positive Electrode</th>
                    </tr>

                    <tr>
                        <th className="parameter_names">Solid Phase Diffusivity [<em>m<sup>2</sup>s<sup>-1</sup></em>]</th>
                        <th id="id_parameter_value_diffusivity_p">{Number(simParams["Reference Diffusitivity_p [m^2 s^-1]"]).toExponential()}</th>
                        <th></th>
                        <th id="id_parameter_value_diffusivity_n">{Number(simParams["Reference Diffusitivity_n [m^2 s^-1]"]).toExponential()}</th>
                    </tr>

                    <tr>
                        <th className="parameter_names">Reaction Rate [<em>m<sup>2.5</sup>mol<sup>-0.5</sup>s<sup>-1</sup></em>]</th>
                        <th id="id_parameter_value_reaction_rate_p">{Number(simParams["Reference Rate Constant_p [m^2.5 mol^-0.5 s^-1]"]).toExponential()}</th>
                        <th></th>
                        <th id="id_parameter_value_reaction_rate_n">{Number(simParams["Reference Rate Constant_n [m^2.5 mol^-0.5 s^-1]"]).toExponential()}</th>
                    </tr>

                    <tr>
                        <th className="parameter_names">Particle Radius [<em>m</em>]</th>
                        <th id="id_parameter_value_particle_radius_p">{Number(simParams["Radius_p [m]"]).toExponential()}</th>
                        <th></th>
                        <th id="id_parameter_value_particle_radius_n">{Number(simParams["Radius_n [m]"]).toExponential()}</th>
                    </tr>

                    <tr>
                        <th className="parameter_names">Volume Fraction</th>
                        <th id="id_parameter_value_volume_fraction_p">{simParams["Volume Fraction_p"]}</th>
                        <th id="id_parameter_value_volume_fraction_sep">{simParams["Volume Fraction_sep"]}</th>
                        <th id="id_parameter_value_volume_fraction_n">{simParams["Volume Fraction_n"]}</th>
                    </tr>

                    <tr>
                        <th className="parameter_names">Anodic Transfer Co-efficient</th>
                        <th id="id_parameter_value_anodic_transfer_coefficient_p">{(Number(simParams["Anodic Transfer Coefficient_p"])).toExponential()}</th>
                        <th></th>
                        <th id="id_parameter_value_anodic_transfer_coefficient_n">{(Number(simParams["Anodic Transfer Coefficient_n"])).toExponential()}</th>
                    </tr>

                    <tr>
                        <th className="parameter_names">Cathodic Transfer Co-efficient</th>
                        <th id="id_parameter_value_cathodic_transfer_coefficient_p">{(1 - Number(simParams["Anodic Transfer Coefficient_p"])).toExponential()}</th>
                        <th></th>
                        <th id="id_parameter_value_cathodic_transfer_coefficient_n">{(1 - Number(simParams["Anodic Transfer Coefficient_n"])).toExponential()}</th>
                    </tr>

                    <tr>
                        <th className="parameter_names">Bruggerman Coefficient</th>
                        <th id="id_parameter_value_bruggerman_coefficient_p">{Number(simParams["Bruggerman Coefficient_p"]).toExponential()}</th>
                        <th id="id_parameter_value_bruggerman_coefficient_sep">{Number(simParams["Bruggerman Coefficient_sep"]).toExponential()}</th>
                        <th id="id_parameter_value_bruggerman_coefficient_n">{Number(simParams["Bruggerman Coefficient_n"]).toExponential()}</th>
                    </tr>

                    <tr>
                        <th className="parameter_names">Max. Conc. [<em>mol m<sup>-3</sup></em>]</th>
                        <th id="id_parameter_value_max_conc_p">{simParams["Max. Conc._p [mol m^-3]"]}</th>
                        <th></th>
                        <th id="id_parameter_value_max_conc_n">{simParams["Max. Conc._n [mol m^-3]"]}</th>
                    </tr>

                    <tr>
                        <th className="parameter_names">Cross-section Area [<em>m<sup>2</sup></em>]</th>
                        {/**/}
                        <th className="parameter_values" id="id_parameter_values_cross_section_area_bc" colSpan="3">{simParams["Electrode Area_n [m^2]"]}</th>
                    </tr>
                    <tr>
                        <th className="parameter_names">Density [<em>kg m<sup>-3</sup></em>]</th>
                        <th className="parameter_values" id="id_parameter_values_density_bc" colSpan="3">{simParams["Density_bc [kg m^-3]"]}</th>
                    </tr>
                    <tr>
                        <th className="parameter_names">Volume [<em>m<sup>3</sup></em>]</th>
                        <th className="parameter_values" id="id_parameter_values_volume_bc" colSpan="3">{Number(simParams["Volume_bc [m^3]"]).toExponential()}</th>
                    </tr>
                    <tr>
                        <th className="parameter_names">Specific Heat [<em>J K<sup>-1</sup> kg<sup>-1</sup></em>]</th>
                        <th className="parameter_values" id="id_parameter_values_specific_heat_bc" colSpan="3">{simParams["Specific Heat_bc [J K^-1 kg^-1]"]}</th>
                    </tr>
                    <tr>
                        <th className="parameter_names">Heat Transfer Coefficient [<em>J K<sup>-1</sup> s<sup>-1</sup></em>]</th>
                        <th className="parameter_values" id="id_parameter_heat_transfer_coefficient_bc" colSpan="3">{simParams["Heat Transfer Coefficient_bc [J s^-1 K^-1]"]}</th>
                    </tr>
                    <tr>
                        <th className="parameter_names">Surface Area [<em>m<sup>3</sup></em>]</th>
                        <th className="parameter_values" id="id_parameter_surface_area_bc" colSpan="3">{simParams["Surface Area_bc [m^2]"]}</th>
                    </tr>
                    <tr>
                        <th className="parameter_names">Capacity [<em>A hr</em>]</th>
                        <th className="parameter_values" id="id_parameter_value_capacity_bc" colSpan="3">{simParams["Capacity_bc [A hr]"]}</th>
                    </tr>
                    <tr>
                        <th className="parameter_names">Maximum Potential Cut-off [<em>V</em>]</th>
                        <th className="parameter_values" id="id_parameter_max_potential_value_bc" colSpan="3">{simParams["Maximum Potential Cut-off_bc [V]"]}</th>
                    </tr>
                    <tr>
                        <th className="parameter_names">Minimum Potential Cut-off [<em>V</em>]</th>
                        <th className="parameter_values" id="id_parameter_min_potential_value_bc" colSpan="3">{simParams["Minimum Potential Cut-off_bc [V]"]}</th>
                    </tr>
                    </tbody>
                </table>
            </div>
            <div className='plots'>
                <Suspense fallback={<h1>Loading...</h1>}>
                    <RenderDataPoints xVal={{"Time [s]": tSim}} yVal={{"SOC_n": socNSim}}/>
                    <RenderDataPoints xVal={{"Time [s]": tSim}} yVal={{"SOC_p": socPSim}}/>
                    <RenderDataPoints xVal={{"Time [s]": tSim}} yVal={{"Potential [V]": vSim}}/>
                    <RenderDataPoints xVal={{"Time [s]": tSim}} yVal={{"Temperature [C]": tempSim}}/>
                </Suspense>
            </div>
        </div>


    );
}

export default Sp;