#include <string.h>

// Forward declarations of used functions
void _route_request(char *request, char *response);
unsigned long long _response_score(char *response);

long long _main(void)
{
    unsigned long long responseScore;
    char *responsePtr;
    char *requestPtr;
    char request[292];
    char response[668];
    unsigned int flag;
    char *v7Pointer;
    char v7;

    v7Pointer = &v7;
    flag = 0;
    responsePtr = response;
    strcpy(response, "POST");
    strcpy(responsePtr + 8, "/api/users/2");
    strcpy(responsePtr + 72, "{\"username\":\"robert\"}");
    strcpy(responsePtr + 328, "admin-token");
    requestPtr = request;
    _route_request(responsePtr, request); // Simulates routing request and filling `request` with response
    responseScore = _response_score(requestPtr); // Score may be used for other computations
    return _response_score(requestPtr); // Returns score of the response stored in `request`
}