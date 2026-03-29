unsigned int _main(void)
{
    unsigned int v0;  // [bp-0x10]
    unsigned int v1;  // [bp-0xc]
    unsigned int choice;  // [bp-0x8]
    unsigned int flag;  // [bp-0x4]

    flag = 0;
    choice = 3;
    v1 = 0;
    v0 = choice;
    if (choice == 1)
    {
        v1 = 10;
        return v1;
    }
    else if (v0 == 2)
    {
        v1 = 20;
        return v1;
    }
    else
    {
        v1 = 30;
        return v1;
    }
}

