unsigned int _main(void)
{
    unsigned int v0;  // [bp-0x14]
    unsigned int v1;  // [bp-0x10]
    unsigned int v2;  // [bp-0xc]
    unsigned int flag;  // [bp-0x8]
    unsigned int choice;  // [bp-0x4]

    choice = 0;
    flag = 0;
    v2 = 7;
    v1 = 3;
    v0 = 0;
    while (true)
    {
        if (!flag)
        {
            if (v2 > v1)
                flag = 1;
            else
                flag = 2;
        }
        else
        {
            if (flag == 1)
            {
                v0 = ((v2 - v1) * 2 | v2 - v1 >> 31) & 4294967294;
                flag = 3;
            }
            else
            {
                if (flag == 2)
                {
                    v0 = 3 * (v1 - v2);
                    flag = 3;
                }
                else if (flag == 3)
                {
                    break;
                }
            }
        }
    }
    return v0;
}
