unsigned int _main(void)
{
    unsigned int cur;
    unsigned int v2;
    unsigned int v3;
    unsigned int v4;
    unsigned int v5;
    
    v5 = 2869;
    v4 = v5 & 1; // Check if v5 is odd
    v3 = ((v5 * 0x80000000) | (v5 >> 1)) & 2147483647 & 7; // Extract and mask relevant bits
    v2 = ((v5 * 0x10000000) | (v5 >> 4)) & 268435455 & 15; // Extract and mask relevant bits
    cur = 0;
    if (v4)
        cur += 10; // Increment for odd v5
    if (v3 >= 2)
        cur += 3 * v3; // Increment based on bit-masked result
    if (v2 > 5 && (((v5 * 0x1000000) | (v5 >> 8)) & 16777215 & 15) == 3) // Additional condition check
        cur += 20;
    return cur;
}