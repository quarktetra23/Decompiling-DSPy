#include <stdio.h>

int main(void)
{
    int count = 3;
    int price = 12;
    int total = count * price;

    printf("items=%d total=%d\n", count, total);

    if (total > 30) {
        return 1;
    }

    return 0;
}