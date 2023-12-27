#include <time.h>
#include <stdio.h>
#include <x86intrin.h>
#include "simd.h"

long long int sum(int vals[NUM_ELEMS]) {
	clock_t start = clock();

	long long int sum = 0;
	for(unsigned int w = 0; w < OUTER_ITERATIONS; w++) {
		for(unsigned int i = 0; i < NUM_ELEMS; i++) {
			if(vals[i] >= 128) {
				sum += vals[i];
			}
		}
	}
	clock_t end = clock();
	printf("Time taken: %Lf s\n", (long double)(end - start) / CLOCKS_PER_SEC);
	return sum;
}

long long int sum_unrolled(int vals[NUM_ELEMS]) {
	clock_t start = clock();
	long long int sum = 0;

	for(unsigned int w = 0; w < OUTER_ITERATIONS; w++) {
		for(unsigned int i = 0; i < NUM_ELEMS / 4 * 4; i += 4) {
			if(vals[i] >= 128) sum += vals[i];
			if(vals[i + 1] >= 128) sum += vals[i + 1];
			if(vals[i + 2] >= 128) sum += vals[i + 2];
			if(vals[i + 3] >= 128) sum += vals[i + 3];
		}

		//This is what we call the TAIL CASE
		//For when NUM_ELEMS isn't a multiple of 4
		//NONTRIVIAL FACT: NUM_ELEMS / 4 * 4 is the largest multiple of 4 less than NUM_ELEMS
		for(unsigned int i = NUM_ELEMS / 4 * 4; i < NUM_ELEMS; i++) {
			if (vals[i] >= 128) {
				sum += vals[i];
			}
		}
	}
	clock_t end = clock();
	printf("Time taken: %Lf s\n", (long double)(end - start) / CLOCKS_PER_SEC);
	return sum;
}

long long int sum_simd(int vals[NUM_ELEMS]) {
	clock_t start = clock();
	__m128i _127 = _mm_set1_epi32(127);		// This is a vector with 127s in it... Why might you need this?
	long long int result = 0;				   // This is where you should put your final result!
	/* DO NOT DO NOT DO NOT DO NOT WRITE ANYTHING ABOVE THIS LINE. */
	
	for(unsigned int w = 0; w < OUTER_ITERATIONS; w++) {
		/* YOUR CODE GOES HERE */
		__m128i total =  _mm_setzero_si128();
		for(unsigned int i = 0; i < NUM_ELEMS/ 4 * 4; i += 4) {
			__m128i* p = (__m128i *) (vals + i);
			__m128i loa = _mm_loadu_si128(p);
			__m128i m = _mm_cmpgt_epi32(loa, _127);
			__m128i done = _mm_and_si128(loa, m);
			total = _mm_add_epi32(total, done);
		}
		int array[4];
		_mm_storeu_si128((__m128i *) array, total);
		int intTotal = array[0] + array[1] + array[2] + array[3];
		result += intTotal;
		/* You'll need a tail case. */
		for(unsigned int i = NUM_ELEMS / 4 * 4; i < NUM_ELEMS; i++) {
			if (vals[i] >= 128) {
				result += vals[i];
			}
		}
	}
	clock_t end = clock();
	printf("Time taken: %Lf s\n", (long double)(end - start) / CLOCKS_PER_SEC);
	return result;
}

long long int sum_simd_unrolled(int vals[NUM_ELEMS]) {
	clock_t start = clock();
	__m128i _127 = _mm_set1_epi32(127);
	long long int result = 0;
	for(unsigned int w = 0; w < OUTER_ITERATIONS; w++) {
		/* COPY AND PASTE YOUR sum_simd() HERE */
		/* MODIFY IT BY UNROLLING IT */
		__m128i total =  _mm_setzero_si128();
		for(unsigned int i = 0; i < NUM_ELEMS/ 16 * 16; i += 16) {
			__m128i* p0 = (__m128i *) (vals + i);
			__m128i* p1 = (__m128i *) (vals + i + 4);
			__m128i* p2 = (__m128i *) (vals + i + 8);
			__m128i* p3 = (__m128i *) (vals + i + 12);
			__m128i loa0 = _mm_loadu_si128(p0);
			__m128i loa1 = _mm_loadu_si128(p1);
			__m128i loa2 = _mm_loadu_si128(p2);
			__m128i loa3 = _mm_loadu_si128(p3);
			
			__m128i m0 = _mm_cmpgt_epi32(loa0, _127);
			__m128i m1 = _mm_cmpgt_epi32(loa1, _127);
			__m128i m2 = _mm_cmpgt_epi32(loa2, _127);
			__m128i m3 = _mm_cmpgt_epi32(loa3, _127);

			__m128i done0 = _mm_and_si128(loa0, m0);
			__m128i done1 = _mm_and_si128(loa1, m1);
			__m128i done2 = _mm_and_si128(loa2, m2);
			__m128i done3 = _mm_and_si128(loa3, m3);


			total = _mm_add_epi32(total, done0);
			total = _mm_add_epi32(total, done1);
			total = _mm_add_epi32(total, done2);
			total = _mm_add_epi32(total, done3);
			
		}
		int array[4];
		_mm_storeu_si128((__m128i *) array, total);
		int intTotal = array[0] + array[1] + array[2] + array[3];
		result += intTotal;
		/* You'll need a tail case. */
		for(unsigned int i = NUM_ELEMS / 16 * 16; i < NUM_ELEMS; i++) {
			if (vals[i] >= 128) {
				result += vals[i];
			}
		}
		/* You'll need 1 or maybe 2 tail cases here. */

	}
	clock_t end = clock();
	printf("Time taken: %Lf s\n", (long double)(end - start) / CLOCKS_PER_SEC);
	return result;
}
