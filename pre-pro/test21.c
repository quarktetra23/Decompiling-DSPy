int main(void)
{
    const char *text = "drugA:Phase2;drugB:Preclinical;drugC:Phase3;";
    int phase_count = 0;
    int i = 0;

    while (text[i] != '\0') {
        if (
            text[i] == 'P' &&
            text[i + 1] == 'h' &&
            text[i + 2] == 'a' &&
            text[i + 3] == 's' &&
            text[i + 4] == 'e'
        ) {
            phase_count++;
        }

        while (text[i] != ';' && text[i] != '\0') {
            i++;
        }

        if (text[i] == ';') {
            i++;
        }
    }

    return phase_count;
}