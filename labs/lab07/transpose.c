#include "transpose.h"

/* The naive transpose function as a reference. */
void transpose_naive(int n, int blocksize, int *dst, int *src) {
    for (int x = 0; x < n; x++) {
        for (int y = 0; y < n; y++) {
            dst[y + x * n] = src[x + y * n];
        }
    }
}

/* Implement cache blocking below. You should NOT assume that n is a
 * multiple of the block size. */
void transpose_blocking(int n, int blocksize, int *dst, int *src) {
    for( int i = 0; i <= n/blocksize; i++ ) {
        for( int j = 0; j <= n/blocksize; j++ ) {
            for( int x = 0; x < blocksize; x++ ) {
               for( int y = 0; y < blocksize; y++ ) {
               	   if((blocksize*i) + x >= n || (blocksize*j) + y >= n) {
               	   	;
               	   } else {
               	   	  dst[(blocksize * j * n) + (blocksize * i) + (y * n) + x] 
               	   	  = src[(blocksize * i * n) + (blocksize * j) + (x * n) + y] ;
               	   }
            	} 
            }
        }
    }
}