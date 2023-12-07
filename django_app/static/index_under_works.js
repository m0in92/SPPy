"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
let normalHeading = "Welcome to the simulation portal.";
let spHeading = "Single Particle Model";
let underConstructionHeading = "Under Construction";
// The following variables store the strings for the descriptions
let welcomeDescription = "Please hover on the items on the left for a basic description. Click on them to be redirected to the " +
    "relevant simulations page.";
let spDescription = "Outputs the battery cell voltage, electrode SOC, and lumped thermal profile from parameter-set " +
    "values.";
let underConstructionDescription = "";
// The following lines are for initial welcome message when the webpage is freshly loaded.
let headingElement = document.getElementById("id_h3_description");
let paraElement = document.getElementById("id_p_description");
headingElement.textContent = normalHeading;
paraElement.textContent = welcomeDescription;
function describe(x, headingText, paraText, imgOptions) {
    let headingElement = document.getElementById("id_h3_description");
    let paraElement = document.getElementById("id_p_description");
    let imgElement = document.getElementById("id_img");
    headingElement.textContent = headingText;
    paraElement.textContent = paraText;
    if (imgOptions == true)
        imgElement.style.display = 'block';
}
function normalDescription(x) {
    let paraElement = document.getElementById("id_p_description");
    let headingElement = document.getElementById("id_h3_description");
    let imgElement = document.getElementById("id_img");
    headingElement.textContent = normalHeading;
    paraElement.textContent = welcomeDescription;
    imgElement.style.display = 'none';
}
