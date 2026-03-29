unsigned int _main(void)
{
    unsigned int i;  // [bp-0x8]
    unsigned int flag;  // [bp-0x4]

    flag = 0;
    for (i = 0; 10 > i; i += 1);
    return i;
}

