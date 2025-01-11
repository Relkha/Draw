#include <stdio.h>
#include <stdlib.h>

void test(int i){
    i +=1;
    printf("%d\n", i);
}

int main() {
    int c = 10;
    test (c);
    return 0;
}
