#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#if INTPTR_MAX == INT32_MAX
    #define THIS_IS_32_BIT_ENVIRONMENT
#elif INTPTR_MAX == INT64_MAX
    #define THIS_IS_64_BIT_ENVIRONMENT
#else
    #error "Environment not 32 or 64-bit."
#endif

int main()
{
  #ifdef THIS_IS_32_BIT_ENVIRONMENT
  printf("32\n" );
  #endif

  #ifdef THIS_IS_64_BIT_ENVIRONMENT
  printf("64\n");
  printf("rand max %d\n", RAND_MAX);
  #endif

}
