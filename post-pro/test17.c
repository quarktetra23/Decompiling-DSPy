unsigned int _main(void)
{
    char v0;  // [bp-0x9]
    unsigned int v1;  // [bp-0x8]
    unsigned int flag;  // [bp-0x4]

    flag = 0;
    v1 = 305419896;
    v0 = v1;
    v0 += 5;
    v1 = v1 & 0xffffff00 | v0;
    if ((char)v1 != 125)
    {
        flag = 0;
        return flag;
    }
    flag = 1;
    return flag;
}
