unsigned int _main(void)
{
    unsigned int index;
    unsigned int status;

    status = 0;
    for (index = 0; index < 10; index += 1); // Loop from 0 to 9
    return index; // Returns 10, as 'index' is incremented after the last iteration
}