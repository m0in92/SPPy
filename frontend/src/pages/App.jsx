import '../css/App.css';
import {lazy, Suspense} from "react";
import { Route, Routes } from "react-router-dom";

import Header from "../componenets/Header";
import Footer from "../componenets/Footer";
//import NavSimsOptions from "./NavSimsOptions";
const NavSimsOptions = lazy(() => import("./NavSimsOptions"));
const Sp = lazy(() => import("./Sp"));
const Ecm = lazy(() => import("./Ecm"));
//import Sp from "./Sp";
//import Ecm from "./Ecm";


function App() {
  return (
    <div className="App">
      <Header/>
        {/*https://stackoverflow.com/questions/34607841/react-router-nav-bar-example
        https://ui.dev/react-router-custom-link
        https://ui.dev/react-router-tutorial*/}
      <Suspense fallback={<h1>Loading...</h1>}>
          <Routes>
            <Route path="" element={<NavSimsOptions />}>

            </Route>
            <Route path="/batterysim/sp" element={<Sp />}>

            </Route>
            <Route path="/batterysim/ecm" element={<Ecm />}>

            </Route>
              {/* Routes that needs a navbar will need to go as children of this Route component */}
          </Routes>

        {/* Routes without a navbar you can add them here as normal routes */}
      </Suspense>
      <Footer/>
    </div>
  );
}

export default App;
