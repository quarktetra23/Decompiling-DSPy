int main(void)
{
    const char *csv = "name,phase\na,1\nb,2\nc,3\nd,P\ne,2\n";
    int i = 0;
    int column = 0;
    int valid_late_stage = 0;

    while (csv[i] != '\0') {
        if (csv[i] == ',') {
            column = column + 1;
        } else if (csv[i] == '\n') {
            column = 0;
        } else if (column == 1) {
            if (csv[i] == '2' || csv[i] == '3') {
                valid_late_stage = valid_late_stage + 1;
            }
        }

        i = i + 1;
    }

    return valid_late_stage;
}
