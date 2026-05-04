unsigned int _main(void)
{
    int v0;  // [bp-0x2c]
    unsigned int v1;  // [bp-0x28]
    int i;  // [bp-0x24]
    int v3;  // [bp-0x20]
    unsigned long long v4;  // [bp-0x10]
    unsigned int v5;  // [bp-0x4]

    v5 = 0;
    v3 = 79228162588051313892677124099;
    v4 = 38654705669;
    i = 0;
    v1 = 0;
    for (v0 = 0; 6 > i; i += 1)
    {
        v1 += *((int *)((char *)&v3 + 4 * i));
        v0 += (i + 1) * *((int *)((char *)&v3 + 4 * i));
    }
    if (v0 <= 70)
    {
        v5 = v1;
        return v5;
    }
    v5 = v0 - v1;
    return v5;
}
