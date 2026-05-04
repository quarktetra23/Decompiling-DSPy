unsigned int _main(void)
{
    unsigned int cur;  // [bp-0x14]
    char *v2;  // [bp-0x10]
    unsigned int v0;  // [bp-0x4]

    v2 = "drug-a Phase 1; drug-b Preclinical; drug-c Phase 2; drug-d Discovery;";
    cur = 0;
    v0 = 0;
    while (v2[cur])
    {
        // Check for the substring "Phase" and increment counter
        if (v2[cur] == 'P' && v2[1 + cur] == 'h' && v2[2 + cur] == 'a' && v2[3 + cur] == 's' && v2[4 + cur] == 'e')
        {
            v0 += 1;
            cur += 5;  // Move past the matched substring
        }
        else
        {
            cur += 1;
        }
    }
    return v0;
}