unsigned int _main(void)
{
    unsigned long v0;  // [bp-0x30]
    unsigned long v1;  // [bp-0x28]
    unsigned int v2;  // [bp-0x20]
    unsigned int v3;  // [bp-0x1c]
    unsigned int v4;  // [bp-0x18]
    unsigned int flag;  // [bp-0x14]
    char *v6;  // [bp-0x10]
    char v7;  // [bp+0x0]

    v6 = &v7;
    flag = 0;
    v4 = 3;
    v3 = 12;
    v2 = v3 * v4;
    v0 = v4;
    v1 = v2;
    _printf("items=%d total=%d\n");
    if (v2 <= 30)
    {
        flag = 0;
        return flag;
    }
    flag = 1;
    return flag;
}
