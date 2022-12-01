const fs = require('fs');

var input = fs.readFileSync('./input.in').toString().split(/\r?\n/);

getFullDraw = input => {
    return input[0].split(',').map(x => parseInt(x));
}

getBoards = input => {
    var boards = [];
    i = 2;
    while (i < input.length - 1) {
        var rawBoard = input.slice(i, i + 5).map(x => x.trim().split(/\s+/).map(y => parseInt(y)));
        boards.push(rawBoard);
        i += 6;
    }
    return boards;
}

checkRows = (board, draw) => {
    for (var row of board) {
        if (row.every(val => draw.has(val))) {
            return true;
        }
    }
    return false;
}

checkBoard = (board, draw) => {
    var rowsWin = checkRows(board, draw);
    if (rowsWin) return true;

    var transposedBoard = board.map((_, colIndex) => board.map(row => row[colIndex]));
    var colsWin = checkRows(transposedBoard, draw);
    if (colsWin) return true;

    return false;
}

calcAnswer = (board, draw, finalNum) => {
    var unmarkedNums = board.flat().filter(x => !draw.has(x));
    var unmarkedNumsSum = unmarkedNums.reduce((x, y) => x + y);

    return unmarkedNumsSum * finalNum;
}

var fullDraw = getFullDraw(input);
var boards = getBoards(input);

part1 = (boards, fullDraw) => {
    var draw = new Set();
    for (num of fullDraw) {
        draw.add(num);
        for (board of boards) {
            var boardWin = checkBoard(board, draw);
            if (boardWin) {
                console.log("Part 1 Answer: %i", calcAnswer(board, draw, num));
                return;
            }
        }
    }
}

part2 = (boards, fullDraw) => {
    var draw = new Set();
    for (num of fullDraw) {
        draw.add(num);
        boardIdxesToRemove = [];
        for (var i = 0; i < boards.length; i++) {
            var board = boards[i];
            if (checkBoard(board, draw)) {
                boardIdxesToRemove.unshift(i);
            }
        }
        potentialLastBoard = boards[0];
        for (idx of boardIdxesToRemove) {
            boards.splice(idx, 1);
        }
        if (boards.length === 0) {
            console.log("Part 2 Answer: %i", calcAnswer(potentialLastBoard, draw, num));
            return;
        }
    }
}

part1(boards, fullDraw);
part2(boards, fullDraw);
