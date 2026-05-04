unsigned int _main(void)
{
    unsigned int v9;  // w8
    unsigned int v0;  // [bp-0x2c]
    unsigned int v1;  // [bp-0x28]
    int v2;  // [bp-0x24]
    unsigned int v3;  // [bp-0x20]
    unsigned int v4;  // [bp-0x1c]
    unsigned int v5;  // [bp-0x18]
    unsigned int i;  // [bp-0x14]
    char *v7;  // [bp-0x10]
    unsigned int v8;  // [bp-0x4]

    v8 = 0;
    v7 = "trial=NCT12345678; status=active; backup=NCT00000001";
    i = 0;
    v5 = 0;
    for (v4 = 0; v7[i]; i += 1)
    {
        if (v7[i] == 78 && v7[1 + i] == 67 && v7[2 + i] == 84)
        {
            v3 = i + 3;
            v2 = 0;
            v1 = 0;
            while (true)
            {
                v0 = 0;
                if (8 > v2)
                {
                    v0 = 0;
                    if (v7[v3] >= 48)
                    {
                        if (57 < v7[v3])
                            v9 = 0;
                        else
                            v9 = 1;
                        v0 = v9;
                    }
                }
                if (!((char)v0 & 1))
                    break;
                v1 += v7[v3] - 48;
                v2 += 1;
                v3 += 1;
            }
            if (v2 == 8)
            {
                v5 = 1;
                v4 = v1;
                break;
            }
        }
    }
    if (!v5)
    {
        v8 = 4294967295;
        return v8;
    }
    v8 = v4;
    return v8;
}
