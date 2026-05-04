int main(void)
{
    int lock = 0;
    int expected = 0;

    if (__sync_bool_compare_and_swap(&lock, expected, 1)) {
        return 1;
    }

    return 0;
}