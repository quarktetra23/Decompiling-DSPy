int main(void)
{
    int choice = 2;
    int result = 0;

    if (choice == 0) {
        result = 5;
    } else if (choice == 1) {
        result = 10;
    } else if (choice == 2) {
        result = 20;
    } else {
        result = -1;
    }

    return result;
}
