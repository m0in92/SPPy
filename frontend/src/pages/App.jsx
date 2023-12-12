import '../css/App.css';
import Header from '../componenets/Header'
import Footer from "../componenets/Footer";
import NavSimsOptions from "../componenets/NavSimsOptions"
import { Outlet, Route, Routes } from "react-router-dom";

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

        {/* Routes without a navbar you can add them here as normal routes */}
      </Routes>
      <Footer/>
    </div>
  );
}

export default App;
