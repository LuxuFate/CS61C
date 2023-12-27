#include "hashtable.h"
#include <stdlib.h>

/*
 * This creates a new hash table of the specified size and with
 * the given hash function and comparison function.
 */
HashTable *createHashTable(int size, unsigned int (*hashFunction)(void *),
                           int (*equalFunction)(void *, void *)) {
  int i = 0;
  HashTable *newTable = malloc(sizeof(HashTable));
  newTable->size = size;
  newTable->data = malloc(sizeof(struct HashBucket *) * size);
  for (i = 0; i < size; i++) {
    newTable->data[i] = NULL;
  }
  newTable->hashFunction = hashFunction;
  newTable->equalFunction = equalFunction;
  return newTable;
}

/*
 * This inserts a key/data pair into a hash table.  To use this
 * to store strings, simply cast the char * to a void * (e.g., to store
 * the string referred to by the declaration char *string, you would
 * call insertData(someHashTable, (void *) string, (void *) string).
 */
void insertData(HashTable *table, void *key, void *data) {
  // 1. Find the right hash bucket location with table->hashFunction.
  // 2. Allocate a new hash bucket struct.
  // 3. Append to the linked list or create it if it does not yet exist.
  
  unsigned int index = ((table->hashFunction)(key)) % (table->size);
  struct HashBucket *bucket = (struct HashBucket *) malloc(sizeof(struct HashBucket));
  if (bucket == NULL){
    exit(1);
  }
  if (table->data[index] != NULL) {
    bucket->next = table->data[index];
  } 
  table->data[index] = bucket;
  bucket->key = key;
  bucket->data = data;
  //printf("Bucket Index: %u\n", index);
  //printf("Bucket Key: %s\n", (char *) table->data[index]->key);
  //printf("Bucket Value: %s\n", (char *) table->data[index]->data);
}

/*
 * This returns the corresponding data for a given key.
 * It returns NULL if the key is not found. 
 */
void *findData(HashTable *table, void *key) {
  // 1. Find the right hash bucket with table->hashFunction.
  // 2. Walk the linked list and check for equality with table->equalFunction.
  unsigned int index = ((table->hashFunction)(key)) % (table->size);
  if (table->data[index] == NULL) {
    return NULL;
  } else {  
    struct HashBucket *buck = table->data[index];
    //printf("Word: %s\n ", key);
    //printf("Bucket Index: %u\n", index);
    //printf("Bucket Key: %s\n", (char *) table->data[index]->key);
    //printf("Bucket Value: %s\n", (char *) table->data[index]->data);
    while(buck != NULL){
      if ((table->equalFunction)(buck->key, key) == 1){
	return buck->data;
      }
      buck = buck->next;
    }
  }
  return NULL;
}


