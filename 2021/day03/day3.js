const fs = require('fs');

var input = fs.readFileSync('./input.in').toString().split(/\r?\n/);

if (input[input.length - 1] === "") {
    input.pop();
}

part1 = input => {
    var gamma_str = "";
    var epsilon_str = "";
    for (var i = 0; i < input[0].length; i++) {
        col = input.map(x => x[i]);

        zeros_count = col.filter(x => x === '0').length;
        ones_count = col.filter(x => x === '1').length;
        most_common = ones_count > zeros_count ? '1' : '0';
        least_common = ones_count > zeros_count ? '0' : '1';

        gamma_str += most_common;
        epsilon_str += least_common;
    }
    gamma = parseInt(gamma_str, 2);
    epsilon = parseInt(epsilon_str, 2);
    console.log("Part 1 answer: %i", gamma * epsilon);
}

filter_once = (vals, i, most_common) => {
    col = vals.map(x => x[i]);

    zeros_count = col.filter(x => x === '0').length;
    ones_count = col.filter(x => x === '1').length;
    if (most_common === true) {
        val_to_choose = ones_count >= zeros_count ? '1' : '0';
    } else {
        val_to_choose = zeros_count <= ones_count ? '0' : '1';
    }

    vals = vals.filter(x => x[i] === val_to_choose);
    return vals;
}

part2 = input => {
    o2_vals = input;
    co2_vals = input;

    // Get O2 value
    for (var i = 0; i < o2_vals[0].length; i++) {
        o2_vals = filter_once(o2_vals, i, true);

        if (o2_vals.length === 1) {
            break;
        }
    }
    o2_str = o2_vals[0];
    o2 = parseInt(o2_str, 2);

    // Get CO2 value
    for (var i = 0; i < co2_vals[0].length; i++) {
        co2_vals = filter_once(co2_vals, i, false);

        if (co2_vals.length === 1) {
            break;
        }
    }
    co2_str = co2_vals[0];
    co2 = parseInt(co2_str, 2);

    console.log("Part 2 answer: %i", o2 * co2);
}

part1(input);
part2(input);
