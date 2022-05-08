const fs = require('fs');

var input = fs.readFileSync('./input.in').toString().split(/\r?\n/).map(x => parseInt(x));

part1 = (input) => {
    count = input.map((measurement, idx) => {
        if (idx != input.length - 1 && input[idx + 1] > measurement) {
            return 1
        }
        return 0
    }).reduce((x, y) => x+y)
    console.log("Part 1 Answer: %i", count)
}

part2 = (input) => {
    count = 0;
    prevSum = input[0] + input[1] + input[2];
    for (var i = 1; i < input.length - 2; i++) {
        var sum = input[i] + input[i+1] + input[i+2]
        if (sum > prevSum) {
            count++;
        }
        prevSum = sum;
    }
    console.log("Part 2 Answer: %i", count);
}

part1(input);
part2(input);
