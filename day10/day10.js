const fs = require('fs');

let input = fs.readFileSync('./input.in').toString().split(/\r?\n/);

if (input[input.length - 1] === '') {
    input.pop();
}

part1 = input => {
    let bracketMap = {
        '(': ')', 
        '[': ']', 
        '{': '}', 
        '<': '>'
    }

    let pointsMap = {
        ')': 3, 
        ']': 57, 
        '}': 1197, 
        '>': 25137
    }

    let totPoints = 0;
    for (let line of input) {
        // Init stack
        let stack = [];

        for (let c of line) {
            // Enumerate through the brackets
            if ('([{<'.includes(c)) {
                stack.push(c);
            } else if (')]}>'.includes(c)) {
                let lastElement = stack.pop();
                if (bracketMap[lastElement] !== c) {
                    // Invalid closing bracket
                    // Add points
                    totPoints += pointsMap[c];
                }
            }
        }
    }

    console.log("Part 1 Answer: %i", totPoints);
}

part2 = input => {
    let bracketMap = {
        '(': ')', 
        '[': ']', 
        '{': '}', 
        '<': '>'
    }

    let pointsMap = {
        '(': 1, 
        '[': 2, 
        '{': 3, 
        '<': 4
    }

    let totPoints = [];
    for (let line of input) {
        // Init stack
        let stack = [];
        let isInvalid = false;
        for (let c of line) {
            // Enumerate through the brackets
            if ('([{<'.includes(c)) {
                // Add to stack if bracket is an opening bracket
                stack.push(c);
            } else if (')]}>'.includes(c)) {
                // Pop from stack if bracket is a closing bracket
                let lastElement = stack.pop();
                if (bracketMap[lastElement] !== c) {
                    // Invalid closing bracket
                    isInvalid = true;
                    break;
                }
            }
        }

        if (!isInvalid) {
            // If the code reaches here, then the line is (in)complete.
            let points = stack.reverse().map(x => pointsMap[x]).reduce((a, b) => 5 * a + b);
            totPoints.push(points);
        }
    }

    // Sort scores and find middle score
    totPoints.sort((a, b) => a - b);
    let winner = totPoints[Math.floor(totPoints.length/2)];

    console.log("Part 2 Answer: %i", winner);
}

part1(input);
part2(input);
