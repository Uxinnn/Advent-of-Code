const fs = require('fs');

let input = fs.readFileSync('./input.in').toString().split(',').map(n => parseInt(n));

if (input[input.length - 1] === "") {
    input.pop();
}

getMedian = input => {
    input.sort((x, y) => x - y);
    let totNumberOfCrabs = input.length;
    let median;
    if (totNumberOfCrabs % 2 === 0) {
        // Even number of crabs
        median = (input[Math.ceil(totNumberOfCrabs / 2)] + input[Math.floor(totNumberOfCrabs / 2)]) / 2;
    } else {
        // Odd number of crabs
        median =  input[Math.floor(totNumberOfCrabs / 2)];
    }
    return median;
}

getTriSum = x => {
    return x * (x + 1) / 2
}

part1 = input => {
    // Minimum distance occurs at median
    let median = getMedian(input);
    let minFuelUsed = input.map(x => Math.abs(x - median)).reduce((x, y) => x + y);
    console.log("Part 1 Answer: %i", minFuelUsed);
}

part2 = input => {
    let minIdx = Math.min(...input);
    let maxIdx = Math.max(...input);
    // Max possible fuel used
    let minFuelUsed = getTriSum(maxIdx - minIdx) * input.length;

    // Iterate through all indices and get the minimum amount of fuel used
    for (let i = minIdx; i < maxIdx + 1; i++) {
        let totFuelUsed = input.map(x => getTriSum(Math.abs(x - i))).reduce((a, b) => a + b);
        if (totFuelUsed < minFuelUsed) {
            minFuelUsed = totFuelUsed;
        }
    }

    console.log("Part 2 Answer: %i", minFuelUsed);
}

part1(input);
part2(input);
