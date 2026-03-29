unsigned int _main(void)
{
    unsigned int maxValue;  // [bp-0xc]
    unsigned int threshold;  // [bp-0x8]
    unsigned int result;  // [bp-0x4]

    result = 0;
    threshold = 5;
    maxValue = 3;
    if (threshold <= maxValue)  // Check if threshold is less than or equal to maxValue
    {
        result = maxValue;  // If true, set result to maxValue
        return result;
    }
    result = threshold;  // If false, set result to threshold
    return result;
}