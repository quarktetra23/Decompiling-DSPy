int main(void)
{
    int values[6] = {3, 1, 4, 1, 5, 9};
    int i = 0;
    int total = 0;
    int weighted = 0;

    while (i < 6) {
        total = total + values[i];
        weighted = weighted + values[i] * (i + 1);
        i = i + 1;
    }

    if (weighted > 70) {
        return weighted - total;
    }

    return total;
}
