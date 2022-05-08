const fs = require('fs');

getStep = (command) => {
    var step;
    if (command[0] == "forward") {
        step = [command[1], 0];
    } else if (command[0] == "down") {
        step = [0, command[1]];
    } else if (command[0] == "up") {
        step = [0, -command[1]];
    }
    return step;
}

move = (loc, command) => {
    if (command[0] == "forward") {
        loc[0] += command[1];
        loc[1] += command[1] * loc[2];
    } else if (command[0] == "down") {
        loc[2] += command[1];
    } else if (command[0] == "up") {
        loc[2] -= command[1];
    }
    return loc;
}

formatCommand = (rawCommand) => {
    var command = rawCommand.split(" ");
    command[1] = parseInt(command[1]);
    return command;
}

var input = fs.readFileSync('./input.in').toString().split(/\r?\n/).map(rawCommand => formatCommand(rawCommand));

part1 = (input) => {
    input = input.map(getStep);
    input = input.slice(0, input.length - 1);
    loc = input.reduce((x, y) => [x[0] + y[0], x[1] + y[1]]);
    answer = loc[0] * loc[1];
    console.log(answer);
}

part2 = (input) => {
    loc = [0, 0, 0];
    for (var i = 0; i < input.length; i++) {
        command = input[i];
        loc = move(loc, command);
    }
    answer = loc[0] * loc[1];
    console.log(answer);
}

part1(input);
part2(input);
