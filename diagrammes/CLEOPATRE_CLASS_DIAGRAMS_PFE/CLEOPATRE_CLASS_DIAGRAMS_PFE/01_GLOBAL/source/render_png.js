#!/usr/bin/env node
/**
 * CLÉOPÂTRE — rendu PNG haute résolution du master SVG (design system premium).
 *
 *   node render_png.js <master.svg> <sortie.png> [largeur_px]
 *
 * Dépendance : @resvg/resvg-js   →   npm i @resvg/resvg-js
 * Les polices (Inter, JetBrains Mono) sont chargées depuis ./fonts, ce qui
 * garantit un rendu identique sur toute machine.
 *
 * Alternatives sans Node :
 *   rsvg-convert -w 2800 -b '#FAFAF9' master.svg -o sortie.png
 *   inkscape --export-type=png --export-width=2800 master.svg
 */
const fs = require("fs");
const path = require("path");
const { Resvg } = require("@resvg/resvg-js");

const [input, output, width = "2800"] = process.argv.slice(2);
if (!input || !output) {
  console.error("usage : node render_png.js <master.svg> <sortie.png> [largeur_px]");
  process.exit(1);
}

const fontDir = path.join(__dirname, "fonts");
const fontFiles = fs.readdirSync(fontDir).map((f) => path.join(fontDir, f));

const resvg = new Resvg(fs.readFileSync(input, "utf8"), {
  font: { fontFiles, loadSystemFonts: false, defaultFontFamily: "Inter" },
  fitTo: { mode: "width", value: parseFloat(width) },
  shapeRendering: 2,
  textRendering: 2,
  background: "#FAFAF9",
});

fs.writeFileSync(output, resvg.render().asPng());
console.log(`PNG écrit : ${output} (largeur ${width} px)`);
