unsigned int _main(void)
{
    unsigned int value;
    unsigned int result;

    value = 305419896;
    // Modify only the least significant byte of 'value' by adding 5
    value = (value & 0xFFFFFF00) | ((unsigned int)((char)value + 5));
    if ((char)value != 125) // Check if the modified byte equals 125
    {
        result = 0; // If not, set result to 0
        return result;
    }
    return 1; // Return 1 if the condition is met
}