int _main(void)
{
    unsigned int v0;  // [bp-0x10]
    int v1;  // [bp-0xc]
    int v2;  // [bp-0x8]
    unsigned int v3;  // [bp-0x4], Other Possible Types: int

    v3 = 0;
    v2 = 14;
    v1 = 21;
    v0 = 0;
    if (v1 > v2)
        v0 = 1;
    else
        v0 = 0;
    if (!v0)
    {
        v3 = v2 - v1;
        return v3;
    }
    v3 = v1 - v2;
    return v3;
}
