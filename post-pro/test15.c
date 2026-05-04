unsigned int _main(void)
{
    unsigned int v0;  // [bp-0x10]
    unsigned int cur;  // [bp-0xc]
    unsigned int v2;  // [bp-0x8]
    unsigned int flag;  // [bp-0x4]

    flag = 0;
    v2 = 7;
    cur = 0;
    v0 = 0;
    while (true)
    {
        if (!v0)
        {
            cur += v2;
            v0 = 1;
        }
        else if (v0 == 2)
        {
            cur = (cur * 2 | cur >> 31) & 4294967294;
            return cur;
        }
        if (cur <= 5)
        {
            cur += 3;
            return cur;
        }
        v0 = 2;
    }
}
