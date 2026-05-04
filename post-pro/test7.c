unsigned int _main(void)
{
    unsigned int v0;  // [bp-0xc]
    unsigned int choice;  // [bp-0x8]
    unsigned int flag;  // [bp-0x4]

    flag = 0;
    choice = 2;
    v0 = 0;
    if (!choice)
    {
        v0 = 5;
        return v0;
    }
    if (choice == 1)
    {
        v0 = 10;
    }
    else
    {
        if (choice == 2)
            v0 = 20;
        else
            v0 = 4294967295;
    }
    return v0;
}
