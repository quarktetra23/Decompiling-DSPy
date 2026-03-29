unsigned int _f(unsigned int a0)
{
    unsigned int v0;  // [bp-0x1c]
    unsigned int v1;  // [bp-0x18]
    char *v2;  // [bp-0x10]
    char v3;  // [bp+0x0]

    v2 = &v3;
    if (1 < a0)
    {
        v0 = _f(a0 - 1);
        v1 = v0 + _f(a0 - 2);
        return v1;
    }
    v1 = a0;
    return v1;
}

unsigned int _main(void)
{
    unsigned int flag;  // [bp-0x14]
    char *v1;  // [bp-0x10]
    char v2;  // [bp+0x0]

    v1 = &v2;
    flag = 0;
    return _f(5);
}

