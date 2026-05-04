int main(void)
{
    int x = 7;
    int y = 0;
    int state = 0;

start:
    if (state == 0) {
        y += x;
        state = 1;
        goto middle;
    }

    if (state == 2) {
        y *= 2;
        goto end;
    }

middle:
    if (y > 5) {
        state = 2;
        goto start;
    } else {
        y += 3;
        goto end;
    }

end:
    return y;
}