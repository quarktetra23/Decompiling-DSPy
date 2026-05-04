unsigned int _main(void)
{
    unsigned int v0;  // [bp-0x18]
    unsigned int cur;  // [bp-0x14]
    char *v2;  // [bp-0x10]
    unsigned int flag;  // [bp-0x4]

    flag = 0;
    v2 = "drug-a Phase 1; drug-b Preclinical; drug-c Phase 2; drug-d Discovery;";
    cur = 0;
    v0 = 0;
    while (v2[cur])
    {
        if (v2[cur] == 80 && v2[1 + cur] == 104 && v2[2 + cur] == 97 && v2[3 + cur] == 115 && v2[4 + cur] == 101)
        {
            v0 += 1;
            cur += 5;
        }
        else
        {
            cur += 1;
        }
    }
    return v0;
}
