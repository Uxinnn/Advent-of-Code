const fs = require('fs');

let input = fs.readFileSync('./input.in').toString().split(/\r?\n/);

if (input[input.length - 1] === '') {
    input.pop();
}

input = input.map(row => row.split('').map(x => parseInt(x)));

// Perform 1 step
doStep = input => {
    let canFlash = [];  // Stores all the octopi that needs to be flashed
    let count = 0;  // Count number of flashes

    // Increment all by 1
    input = input.map(row => row.map(x => x += 1));
    for (let i = 0; i < input.length; i++) {
        for (let j = 0; j < input[0].length; j++) {
            if (input[i][j] === 10) {
                // Means this octopus is ready to flash
                canFlash.push([i, j]);
            }
        }
    }

    while (canFlash && canFlash.length) {
        [i, j] = canFlash.pop();
        input[i][j] = 11;
        count++;
        let surr = [[i - 1, j - 1], [i - 1, j], [i - 1, j + 1], 
                    [i, j - 1], [i, j + 1], 
                    [i + 1, j - 1], [i + 1, j], [i + 1, j + 1]]
        for (coor of surr) {
            if (coor[0] < 0 || coor[0] >= input.length || coor[1] < 0 || coor[1] >= input.length) {
                // Octopus isn't in the grid, skip it
                continue;
            }
            if (input[coor[0]][coor[1]] >= 10) {
                // The octopus has already flashed, skip it
                continue;
            }
            input[coor[0]][coor[1]]++;
            if (input[coor[0]][coor[1]] == 10) {
                // The adjacent flash caused this octopus to be ready to flash
                canFlash.push(coor);
            }
        }
    }

    // Reset all octopi that have flashed
    for (let i = 0; i < input.length; i++) {
        for (let j = 0; j < input[0].length; j++) {
            if (input[i][j] == 11) {
                input[i][j] = 0;
            }
        }
    }

    return [input, count];

}

part1 = input => {
    let totSteps = 100;
    let totFlashes = 0;
    for (let i = 0; i < totSteps; i++) {
        [input, count] = doStep(input);
        totFlashes += count;
    }
    console.log("Part 1 Answer: %i", totFlashes);
}

part2 = input => {
    let count = 0;
    let flashCount = 0;
    while (flashCount !== input.length * input[0].length) {
        [input, flashCount] = doStep(input);
        count++;
    }
    console.log("Part 2 Answer: %i", count);
}

part1(input);
part2(input);
