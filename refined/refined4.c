unsigned int _f(unsigned int a0)
{
    if (a0 > 1)
    {
        // Recursively calculates Fibonacci numbers
        return _f(a0 - 1) + _f(a0 - 2);
    }
    return a0;
}

unsigned int _main(void)
{
    return _f(5); // Calls the Fibonacci function with 5
}