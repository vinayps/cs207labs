#include "bloom.h"

// Borrowed from Bob Jenkins list of hash functions - http://burtleburtle.net/bob/hash/integer.html
index_t hash1(bloom_filter_t *B, key_t k)
{
    k = (k ^ 61) ^ (k >> 16);
    k = k + (k << 3);
    k = k ^ (k >> 4);
    k = k * 0x27d4eb2d;
    k = k ^ (k >> 15);
    return k%TABLE_SIZE;
}

// Borrowed from Bob Jenkins list of hash functions - http://burtleburtle.net/bob/hash/integer.html
index_t hash2(bloom_filter_t *B, key_t k)
{
    k -= (k<<6);
    k ^= (k>>17);
    k -= (k<<9);
    k ^= (k<<4);
    k -= (k<<3);
    k ^= (k<<10);
    k ^= (k>>15);
    return k%TABLE_SIZE;
}

void count_total_one_bits(bloom_filter_t *B)
{
  int count = 0;
  int output_bit = 0;
  for(int i = 0; i < TABLE_SIZE; i++)
  {
    output_bit = get_bit(B, i);
    if(output_bit == 1)
      count += output_bit;
    if(output_bit != 0 && output_bit != 1)
        printf("error  %d %d\n", output_bit, i);
  }
  printf("total count %d\n", count);
}

void set_bit(bloom_filter_t *B, index_t i)
{
  int table_index = i >> 6;
  int bit_index = i % 64;
  uint64_t mask_int = 1ULL << (bit_index-1);
  B->table[table_index] = B->table[table_index] | mask_int;
}

index_t get_bit(bloom_filter_t *B, index_t i)
{
  int table_index = i >> 6;
  int bit_index = i % 64;
  uint64_t mask_int = 1ULL << (bit_index-1);
  return (B->table[table_index] & mask_int) >> (bit_index-1);
}

void bloom_init(bloom_filter_t *B, index_t size_in_bits)
{
  B->size = size_in_bits;
  B->count = 0;
  int number_of_val = B->size >> 6;
  B->table = (index_t *) malloc(number_of_val * sizeof(index_t)); // 64 bit and so 6
  for(int i = 0; i < number_of_val; i++)
    B->table[i] = 0;
}

void bloom_destroy(bloom_filter_t *B)
{
  free(B->table);
  free(B);
  printf("really done\n");
}

void bloom_add(bloom_filter_t *B, key_t k)
{
  int index_from_hash = 0;
  for(int i = 0; i < N_HASHES; i++)
  {
    index_from_hash = ( hash1(B, k) + i*hash2(B, k) ) % TABLE_SIZE;
    set_bit(B, index_from_hash);
  }
}

int bloom_check(bloom_filter_t *B, key_t k)
{
  int index_from_hash = 0;
  for(int i = 0; i < N_HASHES; i++)
  {
    index_from_hash = ( hash1(B, k) + i*hash2(B, k) ) % TABLE_SIZE;
    if( get_bit(B, index_from_hash) != 1 )
      return 0;
  }
  return 1;
}

int * generate_random_arr(int size, int max_value, int seed)
{
  int i;
  int * random_arr;
  random_arr = (int *) malloc(size * sizeof(int));

  /* Intializes random number generator */
  srand((unsigned) seed);

  for(i = 0; i < size; i++)
    random_arr[i] = rand() % max_value;

  return random_arr;
}

int main()
{
  index_t index;
  bloom_filter_t * B;
  B = (bloom_filter_t *) malloc(1 * sizeof(bloom_filter_t));

  bloom_init(B, TABLE_SIZE);

  count_total_one_bits(B);

  int size = 100;
  int * random_arr1, * random_arr2;

  random_arr1 = generate_random_arr(size, 1000000, 1);
  random_arr2 = generate_random_arr(size, 1000000, 2);

  for(int i = 0; i < size; i++)
    bloom_add(B, random_arr1[i]);

  count_total_one_bits(B);

  int false_positives = 0;
  for(int i = 0; i < size; i++)
    false_positives += bloom_check(B, random_arr2[i]);

  printf("False Positives %d\n", false_positives);

  bloom_destroy(B);
  free(random_arr1);
  free(random_arr2);
}

// Results
// 70, 0, 41, 50, 81, 71
// 46, 3, 43, 16, 1, 37
// 1
/*
total count 0
total count 97
False Positives 9 */
// 2
/*
total count 0
total count 181
False Positives 3 */
// 3
/*
total count 0
total count 256
False Positives 0 */
//4
/*
total count 0
total count 320
False Positives 0
*/
// 5
/*
total count 0
total count 375
False Positives 0
*/
