long long _main(void)
{
    unsigned long long v8;  // x0
    long long v0;  // [bp-0x2e8]
    char *v1;  // [bp-0x2e0]
    char *v2;  // [bp-0x2d8]
    char v3;  // [bp-0x2d0]
    char v4;  // [bp-0x1ac]
    unsigned int flag;  // [bp-0x24]
    char *v6;  // [bp-0x10]
    char v7;  // [bp+0x0]

    v6 = &v7;
    flag = 0;
    v1 = &v4;
    ___strcpy_chk(&v4, "POST", 8);
    v0 = 64;
    ___strcpy_chk(v1 + 8, "/api/users/2", 64);
    ___strcpy_chk(v1 + 72, "{\"username\":\"robert\"}", 0x100);
    ___strcpy_chk(v1 + 328, "admin-token", v0);
    v2 = &v3;
    _route_request(v1, &v3);
    v8 = _response_score(v2);
    return _response_score(v2);
}
