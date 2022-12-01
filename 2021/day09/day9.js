const fs = require('fs');

let input = fs.readFileSync('./input.in').toString().split(/\r?\n/);

if (input[input.length - 1] === '') {
    input.pop();
}

input = input.map(x => x.split('').map(y => parseInt(y)));

addBoundaries = heightMap => {
    let maxVal = 10;
    let rowBoundary = new Array(input[0].length + 2).fill(maxVal);
    heightMap = heightMap.map(row => {
        row.unshift(maxVal);
        row.push(maxVal);
        return row;
    })
    heightMap.unshift(rowBoundary);
    heightMap.push(rowBoundary);
    return heightMap;
}

floodFill = (heightMap, col, row, size) => {
    if (heightMap[col][row] > 8) {
        return size;
    }
    heightMap[col][row] = 9;

    let topSize = floodFill(heightMap, col - 1, row, size + 1);
    let rightSize = floodFill(heightMap, col, row + 1, topSize);
    let botSize = floodFill(heightMap, col + 1, row, rightSize);
    let leftSize = floodFill(heightMap, col, row - 1, botSize);

    return leftSize;
}

getBasinSizes = heightMap => {
    let colLength = heightMap.length;
    let rowLength = heightMap[0].length;
    sizes = [];
    for (let col = 1; col < colLength - 1; col++) {
        for (let row = 1; row < rowLength - 1; row++) {
            if (heightMap[col][row] < 9) {
                size = floodFill(heightMap, col, row, 0);
                sizes.push(size);
            }
        }
    }
    return sizes;
}

part1 = input => {
    let heightMap = addBoundaries(input);
    count = 0;
    let colLength = heightMap.length;
    let rowLength = heightMap[0].length;
    for (let col = 1; col < colLength - 1; col++) {
        for (let row = 1; row < rowLength - 1; row++) {
            let val = heightMap[col][row];
            if (heightMap[col + 1][row] > val && heightMap[col - 1][row] > val && heightMap[col][row + 1] > val && heightMap[col][row - 1] > val) {
                count += (val + 1);
            }
        }
    }
    console.log("Part 1 Answer: %i", count);
}

part2 = input => {
    let heightMap = addBoundaries(input);
    let sizes = getBasinSizes(heightMap);
    sizes.sort((a, b) => b - a);
    console.log("Part 2 Answer: %i", sizes[0] * sizes[1] * sizes[2]);
}

part1(input);
part2(input);
