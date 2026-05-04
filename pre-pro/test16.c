int main(void)
{
    int state = 10;
    int a = 4;
    int b = 9;
    int result = 0;

    while (1) {
        switch (state) {
            case 10:
                result = a + b;
                state = 20;
                break;

            case 20:
                if (result > 10)
                    state = 30;
                else
                    state = 40;
                break;

            case 30:
                result = result * 2;
                state = 50;
                break;

            case 40:
                result = result - 2;
                state = 50;
                break;

            case 50:
                return result;
        }
    }
}