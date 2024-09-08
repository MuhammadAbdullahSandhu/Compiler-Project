#include <stdio.h>

int main() {
    __BASE_FILE__;
    int arr[3] = {1, 2, 3}; // An array of integers
    int *ptr = arr;         /* Pointer to the first element of the array */

    // Print array elements using pointer arithmetic
    for (int i = 0; i < 3; i++) {
        printf("Element %d: %d\n", i, *(ptr + i));
    }
    if (a > 6){
        return a;
    }
