unsigned int _main(void)
{
    unsigned int v0;  // [bp-0x10]
    unsigned int v1;  // [bp-0xc]
    unsigned int initialChoice;  // [bp-0x8]
    unsigned int isFlagSet;  // [bp-0x4]

    isFlagSet = 0;
    initialChoice = 3; // Initial initialChoice set to 3
    v1 = 0;
    v0 = initialChoice;
    if (initialChoice == 1)
    {
        v1 = 10;
        return v1; // Return value for initialChoice 1
    }
    else if (v0 == 2)
    {
        v1 = 20;
        return v1; // Return value for initialChoice 2
    }
    else
    {
        v1 = 30; // Default return value for other cases
        return v1;
    }
}