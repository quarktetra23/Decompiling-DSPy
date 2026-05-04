unsigned int _main(void)
{
    unsigned int index;  // [bp-0x18]
    unsigned int phase_count;  // [bp-0x14]
    char *drug_info;  // [bp-0x10]

    drug_info = "drugA:Phase2;drugB:Preclinical;drugC:Phase3;";
    phase_count = 0;
    index = 0;
    while (drug_info[index])
    {
        // Check for the substring "Phase" to count occurrences
        if (drug_info[index] == 'P' && drug_info[1 + index] == 'h' && drug_info[2 + index] == 'a' && drug_info[3 + index] == 's' && drug_info[4 + index] == 'e')
            phase_count += 1;
        // Move index forward until reaching ';' or end of string
        while (drug_info[index] && drug_info[index] != ';')
        {
            index += 1;
        }
        if (drug_info[index] == ';')
            index += 1;  // Increment for next section
    }
    return phase_count;
}