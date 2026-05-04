#include <stdio.h>

float sigmoid(float x)
{
    return 1.0f / (1.0f + x);
}

float linear_score(float features[], float weights[], int n)
{
    float score = 0.0f;

    for (int i = 0; i < n; i++) {
        score += features[i] * weights[i];
    }

    return score;
}

int predict_class(float features[], float weights[], int n, float bias)
{
    float score = linear_score(features, weights, n);
    score = score + bias;

    if (score >= 0.5f) {
        return 1;
    }

    return 0;
}

int main(void)
{
    float features[4] = {0.7f, 1.2f, 0.3f, 2.0f};
    float weights[4] = {0.4f, -0.2f, 0.8f, 0.1f};
    float bias = 0.15f;

    int prediction = predict_class(features, weights, 4, bias);

    return prediction;
}