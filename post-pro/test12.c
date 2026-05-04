unsigned int _main(void)
{
    unsigned int cur;  // [bp-0x1c]
    unsigned int v1;  // [bp-0x18]
    unsigned int v2;  // [bp-0x14]
    unsigned int v3;  // [bp-0x10]
    unsigned int v4;  // [bp-0xc]
    unsigned int v5;  // [bp-0x8]
    unsigned int flag;  // [bp-0x4]

    flag = 0;
    v5 = 2869;
    v4 = v5 & 1;
    v3 = (v5 * 0x80000000 | v5 >> 1) & 2147483647 & 7;
    v2 = (v5 * 0x10000000 | v5 >> 4) & 268435455 & 15;
    v1 = (v5 * 0x1000000 | v5 >> 8) & 16777215 & 15;
    cur = 0;
    if (v4)
        cur += 10;
    if (v3 >= 2)
        cur += 3 * v3;
    if (v2 > 5 && v1 == 3)
        cur += 20;
    return cur;
}
