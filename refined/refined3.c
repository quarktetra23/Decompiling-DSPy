#include <stdio.h> // Include standard input/output library

int entry(void) { // Define function 'entry' that returns an integer
    int total = 0; // Initialize variable 'total' to 0

    for (int index = 0; index < 5; index++) { // Loop from 0 to 4
        total += index; // Add the current value of 'index' to 'total'
    }

    return total; // Return the final value of 'total'
}