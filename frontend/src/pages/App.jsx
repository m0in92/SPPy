import '../css/App.css';
import { Outlet, Route, Routes } from "react-router-dom";

import Header from "../componenets/Header";
import Footer from "../componenets/Footer";
import NavSimsOptions from "./NavSimsOptions";
import Sp from "./Sp";


function App() {
  return (
    <div className="App">
      <Header/>
        <div>
          I HATE REACT!!1!1!! Zucc plz dont kill me
        </div>
        {/*https://stackoverflow.com/questions/34607841/react-router-nav-bar-example
        https://ui.dev/react-router-custom-link
        https://ui.dev/react-router-tutorial*/}
      <Routes>
          {/* Routes that needs a navbar will need to go as children of this Route component */}
        <Route path="" element={<NavSimsOptions />}>

        </Route>
        <Route path="/batterysim/sp" element={<Sp />}>

        </Route>

        {/* Routes without a navbar you can add them here as normal routes */}
      </Routes>
      <Footer/>
    </div>
  );
}

export default App;
