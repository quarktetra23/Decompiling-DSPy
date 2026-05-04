int main(void)
{
    int x = 14;
    int y = 21;
    int flag = 0;

    if (x < y) {
        flag = 1;
    } else {
        flag = 0;
    }

    if (flag) {
        return y - x;
    } else {
        return x - y;
    }
}
