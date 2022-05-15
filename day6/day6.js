const fs = require('fs');

let input = fs.readFileSync('./input.in').toString().split(',').map(n => parseInt(n));

if (input[input.length - 1] === "") {
    input.pop();
}

simulate1Day = counter => {
    for (let j = -1; j < 8; j++) {
        counter[j] = counter[j + 1];
    }
    counter[6] += counter[-1];
    counter[8] = counter[-1];
    counter[-1] = 0;
}

simulateNDays = days => {
    let counter = {}
    for (let i = 0; i < 9; i++) {
        counter[i] = input.filter(n => n == i).length;
    }

    for (let i = 0; i < days; i++) {
        // Simulate 1 day
        simulate1Day(counter);
    }

    return counter;
}

part1 = input => {
    let counter = simulateNDays(80);
    let total_fish = Object.values(counter).reduce((x, y) => x + y);
    console.log(total_fish);
}

part2 = input => {
    let counter = simulateNDays(256);
    let total_fish = Object.values(counter).reduce((x, y) => x + y);
    console.log(total_fish);
}

part1(input);
part2(input);
