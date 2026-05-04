unsigned int _main(void)
{
    unsigned int v0;  // [bp-0x1c]
    unsigned int flag;  // [bp-0x18]
    unsigned int i;  // [bp-0x14]
    char *v3;  // [bp-0x10]
    unsigned int choice;  // [bp-0x4]

    choice = 0;
    v3 = "name,phase\na,1\nb,2\nc,3\nd,P\ne,2\n";
    i = 0;
    flag = 0;
    for (v0 = 0; v3[i]; i += 1)
    {
        if (v3[i] == 44)
        {
            flag += 1;
        }
        else
        {
            if (v3[i] == 10)
            {
                flag = 0;
            }
            else
            {
                if (flag == 1)
                {
                    if (v3[i] == 50 || v3[i] == 51)
                        v0 += 1;
                }
            }
        }
    }
    return v0;
}
