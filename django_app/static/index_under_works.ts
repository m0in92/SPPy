// The following variables store the strings for the subheadings
import {Kinds} from "../../venv/Lib/site-packages/bokeh/server/static/js/lib/core/kinds";
import Null = Kinds.Null;
import Any = Kinds.Any;

let normalHeading: string = "Welcome to the simulation portal.";
let spHeading: string = "Single Particle Model";
let underConstructionHeading: string = "Under Construction";

// The following variables store the strings for the descriptions
let welcomeDescription: string =
    "Please hover on the items on the left for a basic description. Click on them to be redirected to the " +
    "relevant simulations page.";
let spDescription: string =
    "Outputs the battery cell voltage, electrode SOC, and lumped thermal profile from parameter-set " +
    "values.";
let underConstructionDescription: string = "";

// The following lines are for initial welcome message when the webpage is freshly loaded.
let headingElement: HTMLElement | null = document.getElementById("id_h3_description");
let paraElement: HTMLElement | null = document.getElementById("id_p_description");
headingElement!.textContent = normalHeading;
paraElement!.textContent = welcomeDescription;

function describe(x: Any, headingText: string, paraText: string, imgOptions: Boolean) {
    let headingElement: HTMLElement | null = document.getElementById("id_h3_description");
    let paraElement: HTMLElement | null = document.getElementById("id_p_description");
    let imgElement: HTMLElement | null = document.getElementById("id_img");
    headingElement!.textContent = headingText;
    paraElement!.textContent = paraText;
    if (imgOptions == true)
        imgElement!.style.display = 'block';
}

function normalDescription(x: Any) {
    let paraElement: HTMLElement | null = document.getElementById("id_p_description");
    let headingElement: HTMLElement | null = document.getElementById("id_h3_description");
    let imgElement: HTMLElement | null = document.getElementById("id_img");
    headingElement!.textContent = normalHeading;
    paraElement!.textContent = welcomeDescription;
    imgElement!.style.display = 'none';
}