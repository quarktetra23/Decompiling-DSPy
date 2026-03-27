int f(int n){ return n<=1 ? n : f(n-1)+f(n-2); }
int main(){ return f(5); }