unsigned int _main(void)
{
    unsigned int current_value;  // [bp-0xc]

    current_value = 7;
    while (1)
    {
        if (current_value <= 5)
        {
            return current_value + 3;
        }
        // Perform bit manipulation: double the value, incorporate high bits shifted into position, 
        // and ensure the result is even by masking the least significant bit.
        current_value = (current_value * 2 | current_value >> 31) & 4294967294;
        return current_value;
    }
}