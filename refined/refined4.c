#include <stdio.h> // Include standard input-output library

int _f(int param_1) { // Define function _f that takes an integer parameter
    if (param_1 <= 1) return param_1; // Base case: return param_1 if it is 0 or 1
    return _f(param_1 - 1) + _f(param_1 - 2); // Recursive call to calculate Fibonacci
}

void entry(void) { // Define entry point function
    _f(5); // Call _f with an argument of 5
}