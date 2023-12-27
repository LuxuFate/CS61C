/*
 * Include the provided hash table library.
 */
#include "hashtable.h"

/*
 * Include the header file.
 */
#include "philphix.h"

/*
 * Standard IO and file routines.
 */
#include <stdio.h>

/*
 * General utility routines (including malloc()).
 */
#include <stdlib.h>

/*
 * Character utility routines.
 */
#include <ctype.h>

/*
 * String utility routines.
 */
#include <string.h>

/* Functional Prototypes */
char* all_but_first(char *word);
char* all_lower(char *word);

/*
 * This hash table stores the dictionary.
 */
HashTable *dictionary;

/*
 * The MAIN routine.  You can safely print debugging information
 * to standard error (stderr) as shown and it will be ignored in 
 * the grading process.
 */
int main(int argc, char **argv) {
  if (argc != 2) {
    fprintf(stderr, "Specify a dictionary\n");
    return 1;
  }
  /*
   * Allocate a hash table to store the dictionary.
   */
  fprintf(stderr, "Creating hashtable\n");
  dictionary = createHashTable(0x61C, &stringHash, &stringEquals);

  fprintf(stderr, "Loading dictionary %s\n", argv[1]);
  readDictionary(argv[1]);
  fprintf(stderr, "Dictionary loaded\n");

  fprintf(stderr, "Processing stdin\n");
  processInput();

  /*
   * The MAIN function in C should always return 0 as a way of telling
   * whatever program invoked this that everything went OK.
   */
  return 0;
}

/*
 * This should hash a string to a bucket index.  Void *s can be safely cast
 * to a char * (null terminated string)
 */
unsigned int stringHash(void *s) {
  /* Source: djb2 hash function */
  char *str = (char *) s;
  unsigned long hash = 5381;
  int x;
  while (x = *str++) {
    hash = ((hash << 5) + hash) + x;
  }
  return hash;
}

/*
 * This should return a nonzero value if the two strings are identical 
 * (case sensitive comparison) and 0 otherwise.
 */
int stringEquals(void *s1, void *s2) {
  char *str1 = (char *) s1;
  char *str2 = (char *) s2;
  if (strcmp(str1, str2) == 0){
    return 1;
  } else {
    return 0;
  }
}

/*
 * This function should read in every word and replacement from the dictionary
 * and store it in the hash table.  You should first open the file specified,
 * then read the words one at a time and insert them into the dictionary.
 * Once the file is read in completely, return.  You will need to allocate
 * (using malloc()) space for each word.  As described in the spec, you
 * can initially assume that no word is longer than 60 characters.  However,
 * for the final bit of your grade, you cannot assumed that words have a bounded
 * length.  You CANNOT assume that the specified file exists.  If the file does
 * NOT exist, you should print some message to standard error and call exit(61)
 * to cleanly exit the program.
 */
void readDictionary(char *dictName) {
  FILE *file;
  file = fopen(dictName, "r");
  if (file == NULL) {
    fprintf(stderr, "File does not exist.");
    exit(61);     
  }
  char *line = NULL;
  size_t size = 0;
  size_t num_char;
  const char *delimiters = " \t\n";

  num_char = getline(&line, &size, file);  
  while (num_char != -1){
    char *key = (char *) malloc(sizeof(char) * num_char);
    char *value = (char *) malloc(sizeof(char) * num_char);
    if (key == NULL || value == NULL){
      exit(1);
    }
    key = strcpy(key, strtok(line, delimiters));
    value = strcpy(value, strtok(NULL, delimiters));
    //fprintf(stderr, "%s\n", "Inserting:");
    //fprintf(stderr, "Key: %s ", key);
    //fprintf(stderr, "Value: %s\n", value);
    insertData(dictionary, key, value);
   
    num_char = getline(&line, &size, file);
  }
  free(line);
  line = NULL;
  fclose(file);

  //unsigned int index = (dictionary->hashFunction)("ipsum") % (dictionary->size);
  //fprintf(stderr, "%u\n", index);
  //fprintf(stderr, "%s\n", (char*) dictionary->data[index]->data);
}

/*
 * This should process standard input (stdin) and perform replacements as 
 * described by the replacement set then print either the original text or 
 * the replacement to standard output (stdout) as specified in the spec (e.g., 
 * if a replacement set of `taest test\n` was used and the string "this is 
 * a taest of  this-proGram" was given to stdin, the output to stdout should be 
 * "this is a test of  this-proGram").  All words should be checked
 * against the replacement set as they are input, then with all but the first
 * letter converted to lowercase, and finally with all letters converted
 * to lowercase.  Only if all 3 cases are not in the replacement set shoud 
 * it report the original word.
 *
 * Since we care about preserving whitespace and pass through all non alphabet
 * characters untouched, scanf() is probably insufficent (since it only considers
 * whitespace as breaking strings), meaning you will probably have
 * to get characters from stdin one at a time.
 *
 * Do note that even under the initial assumption that no word is longer than 60
 * characters, you may still encounter strings of non-alphabetic characters (e.g.,
 * numbers and punctuation) which are longer than 60 characters. Again, for the 
 * final bit of your grade, you cannot assume words have a bounded length.
 */
void processInput() {
  char *word = (char *) malloc(sizeof(char) * 61);
  if (word == NULL){
    exit(1);
  }
  int word_max = 60;
  int i = 0;
  //fprintf(stderr, "Dictionary size: %d\n", dictionary->size);
  int character;
  while ((character = getchar()) != EOF) {
   // fprintf(stderr, "%c\n", (char *) character);
    if (isalnum(character)){
      if (word_max <= i) {
        fprintf(stderr, "%s\n", "Reallocing"); 
        word_max = word_max * 2;
        word = (char *) realloc(word, sizeof(char) * word_max);
        if (word == NULL){
          exit(1);
        } 
      }
      word[i] = character;
      i++;
      continue;

    } else {
      word[i] = '\0';
      //fprintf(stderr, "Word from input:%s\n", word);
      char *found;
      found = (char *) findData(dictionary, word);
      //fprintf(stderr, "Found normal: %s\n", found);
      if (found != NULL) {
        fprintf(stdout, "%s", found);
	    putchar(character);
        i = 0;
        continue;       
      }
      char *changed1 = all_but_first(word);
      char *found_all_but_first = (char *) findData(dictionary, changed1);
      free(changed1);
      changed1 = NULL;
      if (found_all_but_first != NULL) {
	    //fprintf(stderr, "Inside All but First: %s\n", found_all_but_first);
        fprintf(stdout, "%s", found_all_but_first); 
        putchar(character);	
        i = 0;
        continue;
      }
      char *changed2 = all_lower(word);
      char* found_lower = (char *) findData(dictionary, changed2);
      free(changed2);
      changed2 = NULL;
      if (found_lower != NULL) {
        fprintf(stdout, "%s", found_lower);
        putchar(character);	
        i = 0;
        continue;
      } else {
        fprintf(stdout, "%s", word);
        putchar(character);
        i = 0;	
      }
    } 
    //after else
  }
  //after while
  if (strlen(word) > 0) {
  	word[i] = '\0';
  	//fprintf(stderr, "<%s>\n", word);
    while (1){
    	char *found;
      	found = (char *) findData(dictionary, word);
      	if (found != NULL) {
        	fprintf(stdout, "%s", found);
	    	break;    
      	}
        char *changed1 = all_but_first(word);
      	char *found_all_but_first = (char *) findData(dictionary, changed1);
      	free(changed1);
      	changed1 = NULL;
      	if (found_all_but_first != NULL) {
          	fprintf(stdout, "%s", found_all_but_first); 
          	break;
        }
        char *changed2 = all_lower(word);
        char* found_lower = (char *) findData(dictionary, changed2);
      	free(changed2);
      	changed2 = NULL;
      	if (found_lower != NULL) {
        	fprintf(stdout, "%s", found_lower);
        	break;
      	}
      	fprintf(stdout, "%s", word);
      	break;
    }
  }
  free(word);
  word = NULL;  
}

char* all_but_first(char *word){
  char *copy = (char *) malloc(sizeof(char) * (strlen(word) + 2));
  if (copy == NULL){
    exit(1);
  }
  copy = strcpy(copy, word);
  //fprintf(stderr, "All but first before: %s\n", copy);
  int i = 1;
  if (strlen(copy) > 1) {
    while (copy[i] != '\0') {
      copy[i] = tolower(copy[i]);
      i++;
    }
    copy[i] = '\0';
  }
  //fprintf(stderr, "All but first after: %s\n", copy);
  return copy;
}

char* all_lower(char *word){
  char *copy = (char *) malloc(sizeof(char) * (strlen(word) + 1));
  if (copy == NULL){
    exit(1);
  }
  copy = strcpy(copy, word);
  int i = 0;
  while (copy[i] != '\0') {
    copy[i] = tolower(copy[i]);
    i++;
  }
  copy[i] = '\0';
  return copy;
}
