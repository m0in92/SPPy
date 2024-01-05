import React, {useEffect, useState} from 'react';
import axios from 'axios';
import {API_BASE_URL} from "../constants/constants";

function Sp(){
    const [paramNameList, setParamNameList] = useState([]);
    const [cyclerList, setCyclerList] = useState([]);
    const [socLibInit, setSocLibInit] = useState(0);

    const [paramName, setParamName] = useState('');
    const [cycler, setCycler] = useState('discharge');
    const [simParams, setSimParams] = useState({});

    function handleParamNameUpdate(){
        axios.get(`${API_BASE_URL}/batterysim/sp`, { params: {'parameter_name': paramName}})
            .then((rspn) => {
                setSimParams(JSON.parse(rspn.data["parameter_values"]));
            }).catch((err) => {console.error(err);
      });
    }

    useEffect(() => {
        axios.options(`${API_BASE_URL}/batterysim/sp`)
            .then((rspn) => {
                setParamNameList(rspn.data["sp_options"]["parameter_name_list"]);
                setCyclerList(rspn.data["sp_options"]["cycler_list"]);
                setSocLibInit(rspn.data["sp_options"]["soc_lib_init"]);
                setParamName(rspn.data["sp_options"]["parameter_name_list"][0]);
                setCycler(rspn.data["sp_options"]["cycler_list"][0]);
            })
            .catch((err) => {console.error(err);
            });
    }, []);

    console.log(paramNameList)

    function HandlePOST(e){

    }

    var renderedParamNameList = paramNameList.map(item => <option key={item} value={item}> {item} </option>)
    return(

        <div className="container">
            I H8 REACT!!1!
            <form method="post" onSubmit={HandlePOST}>
                <table>
                <tbody>
                    <tr>
                        <td>Parameter Name:</td>
                        <td>
                            <select value={paramName}
                                    onChange={e => {setParamName(e.target.value); handleParamNameUpdate()}}>
                                {renderedParamNameList}
                            </select>
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