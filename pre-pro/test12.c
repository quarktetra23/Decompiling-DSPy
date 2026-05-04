int main(void)
{
    unsigned int packed = 0x00000B35U;
    unsigned int active = packed & 1U;
    unsigned int phase = (packed >> 1) & 7U;
    unsigned int priority = (packed >> 4) & 15U;
    unsigned int region = (packed >> 8) & 15U;
    unsigned int score = 0;

    if (active) {
        score = score + 10U;
    }

    if (phase >= 2U) {
        score = score + phase * 3U;
    }

    if (priority > 5U && region == 3U) {
        score = score + 20U;
    }

    return (int)score;
}
