unsigned int _main(void)
{
    int i;  // [bp-0xc]
    unsigned int v1;  // [bp-0x8]
    unsigned int flag;  // [bp-0x4]

    flag = 0;
    v1 = 0;
    for (i = 0; 5 > i; i += 1)
    {
        v1 += i;
    }
    return v1;
}
