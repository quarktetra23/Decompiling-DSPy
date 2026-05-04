unsigned int _main(void)
{
    unsigned int result;
    unsigned int flag;
    unsigned int index;
    char *data_string;

    data_string = "name,phase\na,1\nb,2\nc,3\nd,P\ne,2\n";
    index = 0;
    flag = 0;
    for (result = 0; data_string[index]; index += 1)
    {
        if (data_string[index] == ',')
        {
            flag += 1; // Increment flag when a comma is found, indicating a new field
        }
        else if (data_string[index] == '\n')
        {
            flag = 0; // Reset flag at the end of a line
        }
        else if (flag == 1)
        {
            if (data_string[index] == '2' || data_string[index] == '3')
                result += 1; // Increment result if the second field contains '2' or '3'
        }
    }
    return result;
}