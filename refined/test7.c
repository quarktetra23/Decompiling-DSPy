unsigned int _main(void)
{
    unsigned int v0;

    if (!2)
    {
        return 5;
    }
    if (2 == 1)
    {
        v0 = 10;
    }
    else
    {
        if (2 == 2)
        {
            v0 = 20;
        }
        else
        {
            v0 = 4294967295;
        }
    }

    return v0;
}