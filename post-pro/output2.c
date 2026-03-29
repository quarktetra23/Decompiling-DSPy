unsigned int _main(void)
{
    unsigned int v0;  // [bp-0xc]
    unsigned int v1;  // [bp-0x8]
    unsigned int v2;  // [bp-0x4]

    v2 = 0;
    v1 = 5;
    v0 = 3;
    if (v1 <= v0)
    {
        v2 = v0;
        return v2;
    }
    v2 = v1;
    return v2;
}

