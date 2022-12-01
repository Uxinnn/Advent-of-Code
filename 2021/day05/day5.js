const fs = require('fs');

var input = fs.readFileSync('./input.in').toString().split(/\r?\n/);

if (input[input.length - 1] === "") {
    input.pop();
}

input = input.map(x => x.split(" -> ").map(y => y.split(',').map(z => parseInt(z))));

markCoor = (coors, coor) => {
    if (coors.hasOwnProperty(coor)) {
        coors[coor] += 1;
    } else {
        coors[coor] = 1;
    }
}

part1 = input => {
    var coors = {};
    for (line of input) {
        // Reorder line
        if (line[0][0] > line[1][0]) {
            [line[0], line[1]] = [line[1], line[0]];  // Swap coors
        }

        // Check which direction the line goes
        if (line[0][0] === line[1][0]) {
            // Vertical line
            var x = line[0][0];
            var from = line[0][1] < line[1][1] ? line[0][1] : line[1][1];
            var to = line[0][1] >= line[1][1] ? line[0][1] : line[1][1];
            for (var i = from; i <= to; i++) {
                markCoor(coors, [x, i]);
            }
        } else if (line[0][1] === line[1][1]) {
            // Horizontal line
            var y = line[0][1];
            var from = line[0][0];
            var to = line[1][0];
            for (var i = from; i <= to; i++) {
                markCoor(coors, [i, y]);
            }
        }
    }
    var count = Object.keys(coors).filter(x => coors[x] > 1).length;
    console.log("Part 1 Answer: %i", count);
}

part2 = input => {
    var coors = {};
    for (line of input) {
        // Reorder line so that first coor always have a less x value 
        // than the second coor.
        if (line[0][0] > line[1][0]) {
            [line[0], line[1]] = [line[1], line[0]];  // Swap coors
        }

        // Check which direction the line goes
        if (line[0][0] === line[1][0]) {
            // Vertical line
            var x = line[0][0];
            var from = line[0][1] < line[1][1] ? line[0][1] : line[1][1]
            var to = line[0][1] >= line[1][1] ? line[0][1] : line[1][1]
            for (var i = from; i <= to; i++) {
                markCoor(coors, [x, i]);
            }
        } else if (line[0][1] === line[1][1]) {
            // Horizontal line
            var y = line[0][1];
            var from = line[0][0]
            var to = line[1][0]
            for (var i = from; i <= to; i++) {
                markCoor(coors, [i, y]);
            }
        } else if (line[0][1] < line[1][1]) {
            // Diagonal top down
            x = line[0][0];
            y = line[0][1];
            for (var i = 0; i <= (line[1][1] - line[0][1]); i++) {
                markCoor(coors, [x + i, y + i]);
            }
        } else if (line[0][1] > line[1][1]) {
            // Diagonal bottom up
            x = line[0][0];
            y = line[0][1];
            for (var i = 0; i <= (line[0][1] - line[1][1]); i++) {
                markCoor(coors, [x + i, y - i]);
            }
        }
    }
    var count = Object.keys(coors).filter(coor => coors[coor] > 1).length;
    console.log("Part 1 Answer: %i", count);
}

part1(input);
part2(input);
