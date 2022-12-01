const fs = require('fs');

let input = fs.readFileSync('./input.in').toString().split(/\r?\n/);

if (input[input.length - 1] === '') {
    input.pop();
}

var sortString = str => {
    return str.split('').sort().join('');
}

input = input.map(x => x.split(' | ').map(y => y.split(' ').map(z => sortString(z))));

// Get the characters in `str` that is not in `substr`
findDiff = (str, substr) => {
    let diff = "";
    for (let c of str) {
        if (!substr.includes(c)) {
            diff += c;
        }
    }
    return diff;
}

getUnkns2Num = unkns => {
    // These encoded numbers have unique lengths
    let enc_1 = unkns.filter(x => x.length === 2)[0];
    let enc_7 = unkns.filter(x => x.length === 3)[0];
    let enc_4 = unkns.filter(x => x.length === 4)[0];
    let enc_8 = unkns.filter(x => x.length === 7)[0];

    // Get list of encoded numbers of length 5
    // Could possibly be number 2, 3, 5
    let enc_len_5 = unkns.filter(x => x.length === 5);

    // Find out which encoded values are numbers 2, 3, 5
    let enc_2;
    let enc_3;
    let enc_5;
    for (enc_output of enc_len_5) {
        if (findDiff(enc_1, enc_output).length === 0) {
            // Only difference between 1 and 3 will have a length of 0
            enc_3 = enc_output;
        } else {
            // Either 2 or 5
            if (findDiff(enc_output, enc_4).length === 3) {
                // Only difference between 2 and 4 will have a length of 3
                enc_2 = enc_output;
            } else {
                // Left number 5
                enc_5 = enc_output;
            }
        }
    }

    // Get list of encoded numbers of length 6
    // Could possibly be number 0, 6, 9
    let enc_len_6 = unkns.filter(x => x.length === 6);

    // Find out which encoded values are numbers 0, 6, 9
    let enc_0;
    let enc_6;
    let enc_9;
    for (enc_output of enc_len_6) {
        if (findDiff(enc_1, enc_output).length === 1) {
            // Only difference between 1 and 6 will have a length of 1
            enc_6 = enc_output;
        } else {
            // Either 0 or 9
            if (findDiff(enc_5, enc_output).length === 0) {
                // Only difference between 5 and 9 will have a length of 0
                enc_9 = enc_output;
            } else {
                // Left 0
                enc_0 = enc_output;
            }
        }
    }

    return {
        [enc_0]: 0, 
        [enc_1]: 1, 
        [enc_2]: 2, 
        [enc_3]: 3, 
        [enc_4]: 4, 
        [enc_5]: 5, 
        [enc_6]: 6, 
        [enc_7]: 7, 
        [enc_8]: 8, 
        [enc_9]: 9, 
    }
}

// Using the mapping from encoded values to numbers found, decode the
// 4 digit number
decodeOutput = (unkns2num, enc_output) => {
    let output = enc_output.map(x => unkns2num[x]).reduce((a, b) => a * 10 + b);
    return output;
}

part1 = input => {
    let count1478 = 0;
    for (let entry of input) {
        count1478 += entry[1].filter(x => x.length === 2 || x.length === 3 || x.length === 4 || x.length === 7).length;
    }
    console.log("Part 1 Answer: %i", count1478);
}

part2 = input => {
    let outputSum = 0;
    for (entry of input) {
        let unkns2num = getUnkns2Num(entry[0]);
        let output = decodeOutput(unkns2num, entry[1]);
        outputSum += output;
    }
    console.log("Part 2 Answer: %i", outputSum);
}

part1(input);
part2(input);
