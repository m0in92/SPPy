import React, {useEffect, useState} from 'react';
import axios from 'axios';
import {API_BASE_URL} from "../constants/constants";

function Sp(){
    const [paramNameList, setParamNameList] = useState([]);
    const [cyclerList, setCyclerList] = useState([]);
    const [socLibInit, setSocLibInit] = useState(0.0);

    const [paramName, setParamName] = useState("Calce_NMC_18650");
    const [cycler, setCycler] = useState('discharge');
    const [simParams, setSimParams] = useState({});

    const [socValidity, setSocValidity] = useState(true)

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

    console.log(paramNameList)

    // WORK ON POST HANDLING NEXT!!!!!!!!!!!!!!!!!!!!!!!1!!!!!!!!1!
    function HandlePOST(e){

    }
    //////////////////////////////////////////////////////////////

    const renderedParamNameList = paramNameList.map(item => <option key={item} value={item}>{item}</option>)
    const renderedCyclerList = cyclerList.map(item => <option key={item} value={item}>{item}</option>)

    const verifySOC = (e) => {
        // There's a concern that if the input isn't a number the number range check will crash
        // Ugly, potential room for improvement
        if (!isNaN(e.target.valueAsNumber)){
            if (e.target.valueAsNumber <= 1.0 && e.target.valueAsNumber >= 0.0){
                setSocValidity(true)
                setSocLibInit(e.target.valueAsNumber)
            }
        } else {
            setSocValidity(false)
        }
    }
    return(

        <div className="container">
            I H8 REACT!!1!
            <form method="post" onSubmit={HandlePOST}>
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
                                   defaultValue={0.0}
                                   inputMode="numeric"
                                   pattern="[0-9]*"
                                   required={true}
                                   onChange={e => verifySOC(e)}/>
                        </label>
                        {socValidity && <span>Input must be a number between 0.0 and 1.0</span>}
                    </td>
                </tr>
                </tbody>
            </table>
            </form>

            {/*<form onSubmit={handleSubmit}>
                <table>
                    {% csrf_token %}
                    {{ form.as_table }}
                </table>
                <button>Submit</button>
            </form>


            <table className="table_parameter_values">
                <tr>
                    <th colSpan="4"><h3 className="table_main_heading" id="table_parameter_values_main_heading"></h3></th>
                </tr>

                <tr>
                    <th></th>
                    <th>Negative Electrode</th>
                    <th>Seperator</th>
                    <th>Positive Electrode</th>
                </tr>

                <!--        Below are the parameters specific for electrode and seperator regions-->
                <tr>
                    <th className="parameter_names">Solid Phase Diffusivity [<em>m<sup>2</sup>s<sup>-1</sup></em>]</th>
                    <th id="id_parameter_value_diffusivity_p">value_p</th>
                    <th></th>
                    <th id="id_parameter_value_diffusivity_n">value_n</th>
                </tr>

                <tr>
                    <th className="parameter_names">Reaction Rate [<em>m<sup>2.5</sup>mol<sup>-0.5</sup>s<sup>-1</sup></em>]</th>
                    <th id="id_parameter_value_reaction_rate_p">value_p</th>
                    <th></th>
                    <th id="id_parameter_value_reaction_rate_n">value_n</th>
                </tr>

                <tr>
                    <th className="parameter_names">Particle Radius [<em>m</em>]</th>
                    <th id="id_parameter_value_particle_radius_p">value_p</th>
                    <th></th>
                    <th id="id_parameter_value_particle_radius_n">value_n</th>
                </tr>

                <tr>
                    <th className="parameter_names">Volume Fraction</th>
                    <th id="id_parameter_value_volume_fraction_p">value_p</th>
                    <th id="id_parameter_value_volume_fraction_sep">value_sep</th>
                    <th id="id_parameter_value_volume_fraction_n">value_n</th>
                </tr>

                <tr>
                    <th className="parameter_names">Anodic Transfer Co-efficient</th>
                    <th id="id_parameter_value_anodic_transfer_coefficient_p">value_p</th>
                    <th></th>
                    <th id="id_parameter_value_anodic_transfer_coefficient_n">value_n</th>
                </tr>

                <tr>
                    <th className="parameter_names">Cathodic Transfer Co-efficient</th>
                    <th id="id_parameter_value_cathodic_transfer_coefficient_p">value_p</th>
                    <th></th>
                    <th id="id_parameter_value_cathodic_transfer_coefficient_n">value_n</th>
                </tr>

                <tr>
                    <th className="parameter_names">Bruggerman Coefficient</th>
                    <th id="id_parameter_value_bruggerman_coefficient_p">value_p</th>
                    <th id="id_parameter_value_bruggerman_coefficient_sep">value_sep</th>
                    <th id="id_parameter_value_bruggerman_coefficient_n">value_n</th>
                </tr>

                <tr>
                    <th className="parameter_names">Max. Conc. [<em>mol m<sup>-3</sup></em>]</th>
                    <th id="id_parameter_value_max_conc_p">value_p</th>
                    <th></th>
                    <th id="id_parameter_value_max_conc_n">value_n</th>
                </tr>

                <!--        General Battery Cell Parameters below-->
                <tr>
                    <th className="parameter_names">Cross-section Area [<em>m<sup>2</sup></em>]</th>
                    <th className="parameter_values" id="id_parameter_values_cross_section_area_bc" colSpan="3">1626</th>
                </tr>
                <tr>
                    <th className="parameter_names">Density [<em>kg m<sup>-3</sup></em>]</th>
                    <th className="parameter_values" id="id_parameter_values_density_bc" colSpan="3">1626</th>
                </tr>
                <tr>
                    <th className="parameter_names">Volume [<em>m<sup>3</sup></em>]</th>
                    <th className="parameter_values" id="id_parameter_values_volume_bc" colSpan="3">3.38e-5</th>
                </tr>
                <tr>
                    <th className="parameter_names">Specific Heat [<em>J K<sup>-1</sup> kg<sup>-1</sup></em>]</th>
                    <th className="parameter_values" id="id_parameter_values_specific_heat_bc" colSpan="3">750</th>
                </tr>
                <tr>
                    <th className="parameter_names">Heat Transfer Coefficient [<em>J K<sup>-1</sup> s<sup>-1</sup></em>]</th>
                    <th className="parameter_values" id="id_parameter_heat_transfer_coefficient_bc" colSpan="3">1</th>
                </tr>
                <tr>
                    <th className="parameter_names">Surface Area [<em>m<sup>3</sup></em>]</th>
                    <th className="parameter_values" id="id_parameter_surface_area_bc" colSpan="3">0.085</th>
                </tr>
                <tr>
                    <th className="parameter_names">Capacity [<em>A hr</em>]</th>
                    <th className="parameter_values" id="id_parameter_value_capacity_bc" colSpan="3">1.65</th>
                </tr>
                <tr>
                    <th className="parameter_names">Maximum Potential Cut-off [<em>V</em>]</th>
                    <th className="parameter_values" id="id_parameter_max_potential_value_bc" colSpan="3">4.2</th>
                </tr>
                <tr>
                    <th className="parameter_names">Minimum Potential Cut-off [<em>V</em>]</th>
                    <th className="parameter_values" id="id_parameter_min_potential_value_bc" colSpan="3">2.5</th>
                </tr>
            </table>*/}
        </div>
    );
}

export default Sp;