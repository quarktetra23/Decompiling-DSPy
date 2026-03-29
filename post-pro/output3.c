int _main(void)
{
    int i;  // [bp-0xc]

    memset(&i, 0, 12);
    for (; 5 > *((unsigned int *)(&i + 0)); *((unsigned int *)&i) = *((unsigned int *)(&i + 0)) + 1)
    {
        *((unsigned int *)&(&i)[4]) = *((unsigned int *)(&i + 4)) + *((unsigned int *)(&i + 0));
    }
    return *((unsigned int *)(&i + 4));
}

