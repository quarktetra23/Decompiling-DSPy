int main(void)
{
    int state = 0;
    int x = 7;
    int y = 3;
    int result = 0;

    while (1) {
        if (state == 0) {
            if (x > y) {
                state = 1;
            } else {
                state = 2;
            }
        } else if (state == 1) {
            result = (x - y) * 2;
            state = 3;
        } else if (state == 2) {
            result = (y - x) * 3;
            state = 3;
        } else if (state == 3) {
            break;
        }
    }

    return result;
}
