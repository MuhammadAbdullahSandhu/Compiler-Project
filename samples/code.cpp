int isPrime(int n) {
    int a = 2;
    if (n <= 1) {
        return n;
    }
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0){

         return i;
         }
    }
    return n;
}