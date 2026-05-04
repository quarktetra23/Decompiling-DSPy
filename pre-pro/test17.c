int main(void)
{
    unsigned int value = 0x12345678;
    unsigned char low = (unsigned char)value;

    low = low + 5;

    value = (value & 0xffffff00) | low;

    if ((value & 0xff) == 0x7d) {
        return 1;
    }

    return 0;
}