#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_BODY 256
#define MAX_USER 64
#define MAX_ROLE 32

typedef struct {
    char method[8];
    char path[64];
    char body[MAX_BODY];
    char token[64];
} Request;

typedef struct {
    int status;
    char content_type[32];
    char body[MAX_BODY];
} Response;

typedef struct {
    int id;
    char username[MAX_USER];
    char role[MAX_ROLE];
    int active;
} User;

int starts_with(const char *text, const char *prefix)
{
    int i = 0;

    while (prefix[i] != '\0') {
        if (text[i] != prefix[i]) {
            return 0;
        }
        i++;
    }

    return 1;
}

int contains(const char *text, const char *needle)
{
    int i = 0;
    int j = 0;

    if (needle[0] == '\0') {
        return 1;
    }

    while (text[i] != '\0') {
        j = 0;

        while (needle[j] != '\0' && text[i + j] == needle[j]) {
            j++;
        }

        if (needle[j] == '\0') {
            return 1;
        }

        i++;
    }

    return 0;
}

int parse_id_from_path(const char *path)
{
    int i = 0;
    int id = 0;
    int found_digit = 0;

    while (path[i] != '\0') {
        if (path[i] >= '0' && path[i] <= '9') {
            found_digit = 1;
            id = id * 10 + (path[i] - '0');
        }
        i++;
    }

    if (!found_digit) {
        return -1;
    }

    return id;
}

int authenticate(const Request *request)
{
    if (strcmp(request->token, "admin-token") == 0) {
        return 2;
    }

    if (strcmp(request->token, "user-token") == 0) {
        return 1;
    }

    return 0;
}

User load_user_by_id(int id)
{
    User user;

    user.id = id;
    user.active = 1;

    if (id == 1) {
        strcpy(user.username, "alice");
        strcpy(user.role, "admin");
    } else if (id == 2) {
        strcpy(user.username, "bob");
        strcpy(user.role, "user");
    } else {
        strcpy(user.username, "guest");
        strcpy(user.role, "unknown");
        user.active = 0;
    }

    return user;
}

void set_response(Response *response, int status, const char *type, const char *body)
{
    response->status = status;
    strcpy(response->content_type, type);
    strcpy(response->body, body);
}

void handle_health(const Request *request, Response *response)
{
    if (strcmp(request->method, "GET") != 0) {
        set_response(response, 405, "application/json", "{\"error\":\"method_not_allowed\"}");
        return;
    }

    set_response(response, 200, "application/json", "{\"status\":\"ok\"}");
}

void handle_get_user(const Request *request, Response *response)
{
    int auth_level = authenticate(request);

    if (auth_level == 0) {
        set_response(response, 401, "application/json", "{\"error\":\"unauthorized\"}");
        return;
    }

    if (strcmp(request->method, "GET") != 0) {
        set_response(response, 405, "application/json", "{\"error\":\"method_not_allowed\"}");
        return;
    }

    int user_id = parse_id_from_path(request->path);

    if (user_id < 0) {
        set_response(response, 400, "application/json", "{\"error\":\"missing_user_id\"}");
        return;
    }

    User user = load_user_by_id(user_id);

    if (!user.active) {
        set_response(response, 404, "application/json", "{\"error\":\"user_not_found\"}");
        return;
    }

    if (strcmp(user.role, "admin") == 0) {
        set_response(response, 200, "application/json", "{\"user\":\"alice\",\"role\":\"admin\"}");
    } else {
        set_response(response, 200, "application/json", "{\"user\":\"bob\",\"role\":\"user\"}");
    }
}

void handle_update_user(const Request *request, Response *response)
{
    int auth_level = authenticate(request);

    if (auth_level < 2) {
        set_response(response, 403, "application/json", "{\"error\":\"forbidden\"}");
        return;
    }

    if (strcmp(request->method, "POST") != 0) {
        set_response(response, 405, "application/json", "{\"error\":\"method_not_allowed\"}");
        return;
    }

    int user_id = parse_id_from_path(request->path);

    if (user_id < 0) {
        set_response(response, 400, "application/json", "{\"error\":\"missing_user_id\"}");
        return;
    }

    if (!contains(request->body, "username")) {
        set_response(response, 422, "application/json", "{\"error\":\"missing_username\"}");
        return;
    }

    if (user_id == 1) {
        set_response(response, 200, "application/json", "{\"updated\":\"alice\"}");
    } else if (user_id == 2) {
        set_response(response, 200, "application/json", "{\"updated\":\"bob\"}");
    } else {
        set_response(response, 404, "application/json", "{\"error\":\"user_not_found\"}");
    }
}

void handle_search(const Request *request, Response *response)
{
    int auth_level = authenticate(request);

    if (auth_level == 0) {
        set_response(response, 401, "application/json", "{\"error\":\"unauthorized\"}");
        return;
    }

    if (strcmp(request->method, "GET") != 0) {
        set_response(response, 405, "application/json", "{\"error\":\"method_not_allowed\"}");
        return;
    }

    if (contains(request->path, "query=phase")) {
        set_response(response, 200, "application/json", "{\"results\":[\"Phase 1\",\"Phase 2\"]}");
    } else if (contains(request->path, "query=user")) {
        set_response(response, 200, "application/json", "{\"results\":[\"alice\",\"bob\"]}");
    } else {
        set_response(response, 200, "application/json", "{\"results\":[]}");
    }
}

void route_request(const Request *request, Response *response)
{
    if (strcmp(request->path, "/health") == 0) {
        handle_health(request, response);
        return;
    }

    if (starts_with(request->path, "/api/users/") && strcmp(request->method, "GET") == 0) {
        handle_get_user(request, response);
        return;
    }

    if (starts_with(request->path, "/api/users/") && strcmp(request->method, "POST") == 0) {
        handle_update_user(request, response);
        return;
    }

    if (starts_with(request->path, "/api/search")) {
        handle_search(request, response);
        return;
    }

    set_response(response, 404, "application/json", "{\"error\":\"not_found\"}");
}

int response_score(const Response *response)
{
    int score = response->status;

    if (contains(response->body, "error")) {
        score += 1000;
    }

    if (strcmp(response->content_type, "application/json") == 0) {
        score += 10;
    }

    return score;
}

int main(void)
{
    Request request;
    Response response;

    strcpy(request.method, "POST");
    strcpy(request.path, "/api/users/2");
    strcpy(request.body, "{\"username\":\"robert\"}");
    strcpy(request.token, "admin-token");

    route_request(&request, &response);

    return response_score(&response);
}