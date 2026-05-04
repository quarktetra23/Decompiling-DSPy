unsigned int _main(void)
{
    unsigned int v5;  // w8
    unsigned int v0;  // [bp-0x1c]
    unsigned int cur;  // [bp-0x18]
    unsigned int v2;  // [bp-0x14]
    char *v3;  // [bp-0x10]
    unsigned int flag;  // [bp-0x4]

    flag = 0;
    v3 = "drugA:Phase2;drugB:Preclinical;drugC:Phase3;";
    v2 = 0;
    cur = 0;
    while (v3[cur])
    {
        if (v3[cur] == 80 && v3[1 + cur] == 104 && v3[2 + cur] == 97 && v3[3 + cur] == 115 && v3[4 + cur] == 101)
            v2 += 1;
        while (true)
        {
            v0 = 0;
            if (v3[cur] != 59)
            {
                if (!v3[cur])
                    v5 = 0;
                else
                    v5 = 1;
                v0 = v5;
            }
            if (!((char)v0 & 1))
                break;
            cur += 1;
        }
        if (v3[cur] == 59)
            cur += 1;
    }
    return v2;
}
