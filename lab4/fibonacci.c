#include <stdio.h>

int fib(int n)
{
 if( n == 1 )
    return 0;
 if( n == 2 )
    return 1;
 return fib(n-1) + fib(n-2);
}

int main()
{
 int fib_value;
 fib_value = fib(8);
 printf("Fibonacci value is %d\n", fib_value);
}

