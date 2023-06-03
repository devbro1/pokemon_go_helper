import {cp_multiplier} from "./cp_multiplier.mjs";
import {POKEDEX} from "./pokemon_data.mjs";

import Tesseract from "node-tesseract-ocr";
import {execSync} from "child_process";
import sharp from "sharp";
import Jimp from "jimp";
import _ from "lodash";

const config = {
    lang: "eng", // default
    oem: 3,
    psm: 3,
};

function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

async function getPixelColor(imagePath, x, y) {
    const image = await Jimp.read(imagePath);
    //console.log(JSON.stringify([x, y]));
    return Jimp.intToRGBA(image.getPixelColor(x, y));
}

async function getIVValue(imagePath) {
    //console.log('asd');
    let x = [
        2, 26, 46, 74, 99, 128, 146, 167, 193, 219, 247, 263, 290, 312, 338,
        360,
    ];
    for (let i = 0; i < 16; i++) {
        let res = await getPixelColor(imagePath, x[i], 10); //TODO: this is not perfect yet

        if (res.b == 121) {
            return 15;
        } else if (res.b == 226) {
            return i;
        }
        //console.log(res);
    }

    throw new Error("could not figure out IV");
}

async function swipeRight() {
    execSync("adb shell input swipe 930 1485 100 1485 100");
}

async function takeScreenshot(filename = "screenshot.png") {
    execSync("adb shell screencap -p /sdcard/screenshot.png");
    execSync("adb pull /sdcard/screenshot.png ./screenshots/" + filename);
}

async function getScreenshotData(filename = "screenshot.png") {
    let rc = {};

    await sharp("./screenshots/" + filename)
        .extract({left: 0, top: 1950, width: 1080, height: 300})
        .toFile("bottom.png");

    let text = await Tesseract.recognize("bottom.png");
    let shift = 0;

    text = text.replaceAll("\r\n", "\n").replaceAll("\n\n", "\n");

    //console.log(JSON.stringify(text));
    if ((text.match(/\n/g) || []).length == 3) {
        shift = -69;
    }

    await sharp("./screenshots/" + filename)
        .extract({left: 298, top: 1039, width: 520, height: 100})
        .toFile("name.png");

    await sharp("./screenshots/" + filename)
        .extract({left: 298, top: 250, width: 520, height: 100})
        .toFile("cp.png");

    await sharp("./screenshots/" + filename)
        .extract({left: 298, top: 1164, width: 520, height: 50})
        .toFile("health.png");

    await sharp("./screenshots/" + filename)
        .extract({left: 138, top: 1730 + shift, width: 353, height: 20})
        .toFile("attack.png");

    await sharp("./screenshots/" + filename)
        .extract({left: 138, top: 1831 + shift, width: 353, height: 20})
        .toFile("defense.png");

    await sharp("./screenshots/" + filename)
        .extract({left: 138, top: 1935 + shift, width: 353, height: 20})
        .toFile("hp.png");

    rc["name"] = await Tesseract.recognize("name.png", {
        "user-words": "pokemon_names.txt",
    });
    rc["cp"] = await Tesseract.recognize("cp.png");
    rc["health"] = await Tesseract.recognize("health.png");

    rc["name"] = rc["name"].replace(")", "").trim().toLowerCase();
    rc["cp"] = rc["cp"]
        .trim()
        .toLowerCase()
        .replace("cp", "")
        .replace("ce", "");
    rc["cp"] = parseInt(rc["cp"]);
    rc["health"] = rc["health"].trim();
    rc["health"] = rc["health"].substr(rc["health"].indexOf("/") + 1);
    rc["health"] = rc["health"].substr(0, rc["health"].indexOf("H"));

    rc["attack"] = await getIVValue("attack.png");
    rc["defense"] = await getIVValue("defense.png");
    rc["hp"] = await getIVValue("hp.png");

    return rc;
}

async function getPokemonData(pokemon_name) {
    return POKEDEX.find((value) => {
        return value.id == pokemon_name;
    });
}

async function getEvolutions(pokemon) {
    return POKEDEX.filter((value) => {
        return value.family.id == pokemon.family.id;
    });
}

async function estimateLevel(pokemon) {
    let rc = false;
    let prod =
        1.0 *
        pokemon.sum.atk *
        Math.pow(pokemon.sum.def, 0.5) *
        Math.pow(pokemon.sum.sta, 0.5);
    _.forEach(cp_multiplier, (cpm) => {
        let cp_guess = (prod * Math.pow(cpm.multiplier, 2)) / 10;
        if (Math.abs(cp_guess - pokemon.cp) < 3) {
            rc = cpm.level;
        }
    });

    return rc;
}

function calculateStatProduct(attack, defense, stamina, max_cp = 10000) {
    let rc = 0;
    for (let key in cp_multiplier) {
        let cpm = cp_multiplier[key];
        const cp =
            (Math.pow(attack, 1) *
                Math.pow(defense, 0.5) *
                Math.pow(stamina, 0.5) *
                Math.pow(cpm.multiplier, 2)) /
            10;

        if (max_cp < cp) {
            break;
        }

        const cp_attack = attack * cpm.multiplier;
        const cp_defense = defense * cpm.multiplier;
        const cp_stamina = stamina * cpm.multiplier;

        rc = cp_attack * cp_defense * cp_stamina;
    }
    return rc;
}

async function calculateMaxStatProduct(pokemon, max_cp) {
    let rc = {
        stat_product: 0,
        level: 0,
        attack: 0,
        defense: 0,
        stamina: 0,
        cp: 0,
        pokemon_name: pokemon.id,
    };

    let rc2 = [];

    _.forEach(cp_multiplier, (cpm) => {
        for (let ind_attack = 0; ind_attack < 16; ind_attack++) {
            for (let ind_defense = 0; ind_defense < 16; ind_defense++) {
                for (let ind_stamina = 0; ind_stamina < 16; ind_stamina++) {
                    const attack = ind_attack + pokemon.stats.atk;
                    const defense = ind_defense + pokemon.stats.def;
                    const stamina = ind_stamina + pokemon.stats.sta;

                    const cp =
                        (Math.pow(attack, 1) *
                            Math.pow(defense, 0.5) *
                            Math.pow(stamina, 0.5) *
                            Math.pow(cpm.multiplier, 2)) /
                        10;

                    if (max_cp < cp) {
                        break;
                    }

                    const cp_attack = attack * cpm.multiplier;
                    const cp_defense = defense * cpm.multiplier;
                    const cp_stamina = stamina * cpm.multiplier;

                    const stat_product = cp_attack * cp_defense * cp_stamina;

                    if (rc.stat_product === stat_product) {
                        rc2.push({
                            level: cpm.level,
                            cp,
                            stat_product,
                            attack,
                            defense,
                            stamina,
                            pokemon_name: pokemon.id,
                        });
                    } else if (rc.stat_product < stat_product) {
                        rc = {
                            level: cpm.level,
                            cp,
                            stat_product,
                            attack,
                            defense,
                            stamina,
                            pokemon_name: pokemon.id,
                        };
                        rc2 = [];
                    }
                }
            }
        }
    });

    if (rc2.length === 0) {
        rc = [rc];
    }

    return rc;
}

function findBest(arr, pokemon) {
    arr = arr.sort((a, b) => {
        if (a.stat_product < b.stat_product) {
            return 1;
        } else if (a.stat_product > b.stat_product) {
            return -1;
        }

        return 0;
    });

    return arr[0];
}

async function outputData() {
    let ind = {cp: "asd"};

    while (isNaN(ind.cp)) {
        await takeScreenshot();
        ind = await getScreenshotData();
    }
    const spokemon = await getPokemonData(ind.name);

    const pokemons = await getEvolutions(spokemon);

    const bests = {little: [], great: [], ultra: []};
    const best = {little: null, great: null, ultra: null};

    const currents = {little: [], great: [], ultra: []};
    const current = {little: null, great: null, ultra: null};

    for (let pokemon of pokemons) {
        pokemon.cp = ind.cp;
        pokemon.ind = {atk: ind.attack, def: ind.defense, sta: ind.hp};
        pokemon.sum = {
            atk: pokemon.stats.atk + ind.attack,
            def: pokemon.stats.def + ind.defense,
            sta: pokemon.stats.sta + ind.hp,
        };
        pokemon.health = ind.health;
        pokemon.level = await estimateLevel(pokemon);
        bests.little.push((await calculateMaxStatProduct(pokemon, 500))[0]);
        bests.great.push((await calculateMaxStatProduct(pokemon, 1500))[0]);
        bests.ultra.push((await calculateMaxStatProduct(pokemon, 2500))[0]);

        currents.little.push(
            calculateStatProduct(
                pokemon.sum.atk,
                pokemon.sum.def,
                pokemon.sum.sta,
                500
            )
        );
        currents.great.push(
            calculateStatProduct(
                pokemon.sum.atk,
                pokemon.sum.def,
                pokemon.sum.sta,
                1500
            )
        );
        currents.ultra.push(
            calculateStatProduct(
                pokemon.sum.atk,
                pokemon.sum.def,
                pokemon.sum.sta,
                2500
            )
        );
    }

    best.little = findBest(bests.little, spokemon);
    best.great = findBest(bests.great, spokemon);
    best.ultra = findBest(bests.ultra, spokemon);

    current.little = findBest(currents.little, spokemon);
    current.great = findBest(currents.great, spokemon);
    current.ultra = findBest(currents.ultra, spokemon);

    // console.log(spokemon);
    // console.log("---------------");
    // console.log(best);
    // console.log("---------------");
    // console.log(current);

    console.log(
        spokemon.name,
        ",",
        spokemon.cp,
        ",",
        ((spokemon.ind.atk + spokemon.ind.def + spokemon.ind.sta)/45).toFixed(2),
        ",",
        spokemon.ind.atk,
        ",",
        spokemon.ind.def,
        ",",
        spokemon.ind.sta,
        ",",
        (current.little / best.little?.stat_product).toFixed(2),
        ",",
        (current.great / best.great?.stat_product).toFixed(2),
        ",",
        (current.ultra / best.ultra?.stat_product).toFixed(2)
    );
}

async function main() {
    for (let i = 0; i < 1000; i++) {
        await outputData();
        await swipeRight();
        await sleep(2000);
    }
    // console.log(await getIVValue('0.png'));
    // console.log(await getIVValue('1.png'));
    // console.log(await getIVValue('2.png'));
    // console.log(await getIVValue('3.png'));
    // console.log(await getIVValue('4.png'));
    // console.log(await getIVValue('5.png'));
    // console.log(await getIVValue('6.png'));
    // console.log(await getIVValue('7.png'));
    // console.log(await getIVValue('8.png'));
    // console.log(await getIVValue('9.png'));
    // console.log(await getIVValue('10.png'));
    // console.log(await getIVValue('11.png'));
    // console.log(await getIVValue('12.png'));
    // console.log(await getIVValue('13.png'));
    // console.log(await getIVValue('14.png'));
    // console.log(await getIVValue('15.png'));
}

main();
