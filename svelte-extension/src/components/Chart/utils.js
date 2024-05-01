// @ts-nocheck
let lastId = 0
export const getUniqueId = (prefix="") => {
    lastId++
    return [prefix, lastId].join("-")
}



// Formats a number as a price string with a '$' sign and shortens large numbers.
// Args:
//     number: The number to format (float).
// Returns:
//     A string representing the formatted price.
export const formatPrice = (number) => {

    const suffixes = ["", "K", "M", "B", "T"];
    const thousand = 1000.0;
    let prefix = "";
  
    // Handle negative numbers
    if (number < 0) {
        prefix = "-";
        number = abs(number);
    }
  
    // Determine the appropriate suffix
    let i = 0;
    while (number >= thousand && i < suffixes.length - 1) {
        number /= thousand;
        i += 1;
    }
  
    // Format the number with two decimal places
    //const formattedNumber = number.toFixed(2);
  
    // Combine prefix, formatted number, suffix, and '$' sign
    return `${prefix}${number}${suffixes[i]}$`;
}