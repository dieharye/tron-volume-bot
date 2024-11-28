const chalk = require('chalk');
const path = require('path');
const fs = require('fs');
const packageJson = require('./package.json');


async function printLogoAscii() {
    const filePath = path.join(__dirname, 'ascii.txt');
    const ascii = fs.readFileSync(filePath, 'utf-8');
    console.log("\n");
    console.log(chalk.redBright(ascii));
    console.log(" ");
    console.log("v" + packageJson.version, "\n");
    console.log(chalk.hex("#a600b5")("by Handsome Finance\n"));
    console.log(chalk.italic("CTRL + C (Control + C on Mac) to exit at any point\n"));
}

async function mainMenu() {
    console.log(chalk.bgGreen("\n               "));
    console.log(chalk.bgGreen("   Main Menu   "));
    console.log(chalk.bgGreen("               \n"));
}

async function main() {
    await mainMenu();
    console.log("Get the full version here:", chalk.green("https://t.me/+glKuxUMA1Pw3ZTM0"))
}

printLogoAscii();
main().catch(console.error);