unsigned int _main(void)
{
    int i;  // [bp-0x1c]
    unsigned int v1;  // [bp-0x18]
    unsigned int flag;  // [bp-0x14]
    char *v3;  // [bp-0x10]
    char v4;  // [bp+0x0]

    v3 = &v4;
    flag = 0;
    v1 = 0;
    for (i = 0; 5 > i; i += 1)
    {
        v1 += _helper(i);
    }
    return v1;
}
