int main(void)
{
    const char *text = "trial=NCT12345678; status=active; backup=NCT00000001";
    int i = 0;
    int found = 0;
    int digit_sum = 0;

    while (text[i] != '\0') {
        if (text[i] == 'N' && text[i + 1] == 'C' && text[i + 2] == 'T') {
            int j = i + 3;
            int digits = 0;
            int sum = 0;

            while (digits < 8 && text[j] >= '0' && text[j] <= '9') {
                sum = sum + (text[j] - '0');
                digits = digits + 1;
                j = j + 1;
            }

            if (digits == 8) {
                found = 1;
                digit_sum = sum;
                break;
            }
        }
        i = i + 1;
    }

    if (found) {
        return digit_sum;
    }

    return -1;
}
