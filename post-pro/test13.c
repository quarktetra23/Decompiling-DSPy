long long _main(void)
{
    int i;  // [bp-0x38]
    unsigned int cur;  // [bp-0x34]
    int v2;  // [bp-0x30]
    uint128_t v3;  // [bp-0x20]
    unsigned int flag;  // [bp-0x4]

    flag = 0;
    v2 = 19807040628695211607043688366092;
    v3 = 237684488299109520180680589331;
    cur = 0;
    for (i = 0; 8 > i; i += 1)
    {
        cur ^= *((int *)((char *)&v2 + 4 * i));
        cur = (cur * 2 | cur >> 31) & 1 | cur * 2;
        if (!((char)*((int *)((char *)&v2 + 4 * i)) & 1))
            cur += 17;
        else
            cur += 31;
    }
    return (char)cur;
}
