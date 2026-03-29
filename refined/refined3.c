#include <string.h>

int main(void)
{
    int counter = 0;  // Initialize to 0
    unsigned int *accumulator = (unsigned int *)&counter;

    for (; counter < 5; counter++)
    {
        accumulator[1] += counter;  // Accumulate the sum of counter in accumulator[1]
    }
    return accumulator[1];  // Return the accumulated value
}