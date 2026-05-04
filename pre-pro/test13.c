int main(void)
{
    unsigned int bytes[8] = {12U, 33U, 7U, 250U, 19U, 88U, 41U, 3U};
    unsigned int checksum = 0U;
    int i = 0;

    while (i < 8) {
        checksum = checksum ^ bytes[i];
        checksum = (checksum << 1) | (checksum >> 31);

        if ((bytes[i] & 1U) == 0U) {
            checksum = checksum + 17U;
        } else {
            checksum = checksum + 31U;
        }

        i = i + 1;
    }

    return (int)(checksum & 255U);
}
