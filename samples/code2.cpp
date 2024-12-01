
int x;
int main() {
    x = 10;
    int y = 10;
    int h = 4 + ( 3- 2);
    if ( x < y ){
        y ++;
    }
    

    return x;
}




int add(int a, int b) {

    int g = 3 + 5;
    return a + b;
}

int main() {
    add(3, 4);  // Expected output: 7

    // Test Case 2
    add(5, 10);  // Expected output: 5

    // Test Case 3
    add(0, 0);  // Expected output: 0

    return 0;
}


int factorial(int n) {
    if (n <= 1){
        return 1;
    }
    return n * factorial(n - 1);
}



int add (int a, int b){
    return a + b;
}

int isPrime(int n) {
    n = 3;
    int a = 2;
    if (n <= 1) {
        return n;
    }
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0){
        add(4+4);
         return i;
         }
    }
    return n;
}



int main() {
    int x = 5;
    int y = x + 10;
    int z;

    if (y > 10) {
        z = 1;
    } else {
        z = 0;
    }

    return z;
}



int add(int a, int b) {

    return a + b;
}

int main() {
    int num1, num2, sum;
    num1 = 4;
    num2 = 5;
    sum = add(num1, num2);
    
    return 0;
}

int sum() {
    int a = 7;
    int b = 6;
    int num;
    if (a > b) {
            num = a + b;
    } else {
        num = a - b;
    }
    return 1;
}