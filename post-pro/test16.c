unsigned int _main(void)
{
    unsigned int v0;  // [bp-0x18]
    unsigned int v1;  // [bp-0x14]
    unsigned int v2;  // [bp-0x10]
    unsigned int v3;  // [bp-0xc]
    unsigned int v4;  // [bp-0x8]
    unsigned int flag;  // [bp-0x4]

    flag = 0;
    v4 = 10;
    v3 = 4;
    v2 = 9;
    v1 = 0;
    while (true)
    {
        v0 = v4;
        if (v4 != 10)
        {
            switch (v0)
            {
            case 20:
                if (v1 > 10)
                    v4 = 30;
                else
                    v4 = 40;
                goto LABEL_100000428;
            case 30:
                v1 = (v1 * 2 | v1 >> 31) & 4294967294;
                v4 = 50;
                goto LABEL_100000428;
            case 40:
                v1 -= 2;
                v4 = 50;
                goto LABEL_100000428;
            case 50:
                return v1;
            default:
LABEL_100000428:
                break;
            }
        }
        else
        {
            v1 = v3 + v2;
            v4 = 20;
            goto LABEL_100000428;
        }
    }
}
