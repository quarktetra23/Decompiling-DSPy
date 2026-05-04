int main(void)
{
    const char *page = "drug-a Phase 1; drug-b Preclinical; drug-c Phase 2; drug-d Discovery;";
    int i = 0;
    int phase_count = 0;

    while (page[i] != '\0') {
        if (page[i] == 'P' && page[i + 1] == 'h' && page[i + 2] == 'a' &&
            page[i + 3] == 's' && page[i + 4] == 'e') {
            phase_count = phase_count + 1;
            i = i + 5;
        } else {
            i = i + 1;
        }
    }

    return phase_count;
}
