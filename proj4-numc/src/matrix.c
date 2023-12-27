#include "matrix.h"
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

// Include SSE intrinsics
#if defined(_MSC_VER)
#include <intrin.h>
#elif defined(__GNUC__) && (defined(__x86_64__) || defined(__i386__))
#include <immintrin.h>
#include <x86intrin.h>
#endif

/* Below are some intel intrinsics that might be useful
 * void _mm256_storeu_pd (double * mem_addr, __m256d a)
 * __m256d _mm256_set1_pd (double a)
 * __m256d _mm256_set_pd (double e3, double e2, double e1, double e0)
 * __m256d _mm256_loadu_pd (double const * mem_addr)
 * __m256d _mm256_add_pd (__m256d a, __m256d b)
 * __m256d _mm256_sub_pd (__m256d a, __m256d b)
 * __m256d _mm256_fmadd_pd (__m256d a, __m256d b, __m256d c)
 * __m256d _mm256_mul_pd (__m256d a, __m256d b)
 * __m256d _mm256_cmp_pd (__m256d a, __m256d b, const int imm8)
 * __m256d _mm256_and_pd (__m256d a, __m256d b)
 * __m256d _mm256_max_pd (__m256d a, __m256d b)
*/

/* Generates a random double between low and high */
double rand_double(double low, double high) {
    double range = (high - low);
    double div = RAND_MAX / range;
    return low + (rand() / div);
}

/* Generates a random matrix */
void rand_matrix(matrix *result, unsigned int seed, double low, double high) {
    srand(seed);
    for (int i = 0; i < result->rows; i++) {
        for (int j = 0; j < result->cols; j++) {
            set(result, i, j, rand_double(low, high));
        }
    }
}

/*
 * Allocates space for a matrix struct pointed to by the double pointer mat with
 * `rows` rows and `cols` columns. You should also allocate memory for the data array
 * and initialize all entries to be zeros. `parent` should be set to NULL to indicate that
 * this matrix is not a slice. You should also set `ref_cnt` to 1.
 * You should return -1 if either `rows` or `cols` or both have invalid values, or if any
 * call to allocate memory in this function fails. If you don't set python error messages here upon
 * failure, then remember to set it in numc.c.
 * Return 0 upon success.
 */
int allocate_matrix(matrix **mat, int rows, int cols) {
    if (rows < 1 || cols < 1) {
        return -1;
    }
    (*mat) = (matrix *)malloc(sizeof(matrix));
    (*mat)->data = (double *)calloc(rows * cols, sizeof(double));
    if (*mat == NULL || (*mat)->data == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "Malloc Failed!");
        return -1;
    }
    (*mat)->rows = rows;
    (*mat)->cols = cols;
    (*mat)->ref_cnt = 1;
    (*mat)->parent = NULL;
    return 0;
}

/*
 * Allocates space for a matrix struct pointed to by `mat` with `rows` rows and `cols` columns.
 * Its data should point to the `offset`th entry of `from`'s data (you do not need to allocate memory)
 * for the data field. `parent` should be set to `from` to indicate this matrix is a slice of `from`.
 * You should return -1 if either `rows` or `cols` or both are non-positive or if any
 * call to allocate memory in this function fails.
 * If you don't set python error messages here upon failure, then remember to set it in numc.c.
 * Return 0 upon success.
 */
int allocate_matrix_ref(matrix **mat, matrix *from, int offset, int rows, int cols) {
    if (rows < 1 || cols < 1) {
        return -1;
    }
    (*mat) = (matrix *)malloc(sizeof(matrix));
    if (mat == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "Malloc Failed!");
        return -1;
    }
    (*mat)->data = from->data + offset;
    (*mat)->rows = rows;
    (*mat)->cols = cols;
    (from)->ref_cnt += 1;
    (*mat)->ref_cnt = from->ref_cnt;
    (*mat)->parent = from;
    return 0;
}

/*
 * You need to make sure that you only free `mat->data` if `mat` is not a slice and has no existing slices,
 * or if `mat` is the last existing slice of its parent matrix and its parent matrix has no other references
 * (including itself). You cannot assume that mat is not NULL.
 */
void deallocate_matrix(matrix *mat) {
    if (mat == NULL) {
        return;
    }
    if (mat->parent == NULL) {
        if (mat->ref_cnt <= 1) {
            free(mat->data);
        } else {
            mat->ref_cnt -= 1;
        }
    } else if (mat->parent != NULL) {
        if (mat->parent->ref_cnt == 1) {
            free(mat->parent->data);
        } else {
            mat->parent->ref_cnt -= 1;
            mat->ref_cnt = 0;
        }
    }
    free(mat);
}

/*
 * Returns the double value of the matrix at the given row and column.
 * You may assume `row` and `col` are valid.
 */
double get(matrix *mat, int row, int col) {
    return mat->data[row * mat->cols + col];
}

/*
 * Sets the value at the given row and column to val. You may assume `row` and
 * `col` are valid
 */
void set(matrix *mat, int row, int col, double val) {
    mat->data[row * mat->cols + col] = val;
}

/*
 * Sets all entries in mat to val
 */
void fill_matrix(matrix *mat, double val) {
    #pragma omp parallel for 
        for (int i = 0; i < mat->rows; i++) {
            for (int j = 0; j < mat->cols; j++) {
                mat->data[i * mat->cols + j] = val;
            }
        }
}

/*
 * Store the result of adding mat1 and mat2 to `result`.
 * Return 0 upon success and a nonzero value upon failure.
 */
int add_matrix(matrix *result, matrix *mat1, matrix *mat2) {
    if ((mat1->rows != mat2->rows) || (mat1->cols != mat2->cols)) {
        return 1;
    }
    int i, j;
    #pragma omp parallel for private(i, j)
        for (i = 0; i < mat1->rows; i++) {
            for (j = 0; j < mat1->cols; j++) {
                __m256d m1 = _mm256_loadu_pd((double *) mat1->data + (i * mat1->cols + j));
                __m256d m2 = _mm256_loadu_pd((double *) mat2->data + (i * mat2->cols + j));
                result->data[i * result->cols + j] = _mm256_add_pd(m1, m2)[0];
                //result->data[i * result->cols + j] = mat1->data[i * mat1->cols + j] + mat2->data[i * mat2->cols + j];
            }
        }
    return 0;
}

/*
 * Store the result of subtracting mat2 from mat1 to `result`.
 * Return 0 upon success and a nonzero value upon failure.
 */
int sub_matrix(matrix *result, matrix *mat1, matrix *mat2) {
    if ((mat1->rows != mat2->rows) || (mat1->cols != mat2->cols)) {
        return 1;
    }
    int i, j;
    #pragma omp parallel for private(i, j)
        for (i = 0; i < mat1->rows; i++) {
            for (j = 0; j < mat1->cols; j++) {
                __m256d m1 = _mm256_loadu_pd((double *) mat1->data + (i * mat1->cols + j));
                __m256d m2 = _mm256_loadu_pd((double *) mat2->data + (i * mat2->cols + j));
                result->data[i * result->cols + j] = _mm256_sub_pd(m1, m2)[0];
                //result->data[i * result->cols + j] = mat1->data[i * mat1->cols + j] - mat2->data[i * mat2->cols + j];
            }
        }
    return 0;
}

/*
 * Store the result of multiplying mat1 and mat2 to `result`.
 * Return 0 upon success and a nonzero value upon failure.
 * Remember that matrix multiplication is not the same as multiplying individual elements.
 */
int mul_matrix(matrix *result, matrix *mat1, matrix *mat2) {
    if ((mat1->cols != mat2->rows)) {
        return 1;
    }
    int c0 = result->cols;
    int r1 = mat1->rows;
    int c1 = mat1->cols;
    int r2 = mat2->rows;
    int c2 = mat2->cols;
    double *mat1_data = mat1->data;
    double *mat2_data = mat2->data;
    double *result_data = result->data;

    if (r1 * c2 < 700) { // 0-24
        for (int i = 0; i < r1; i++) {
            for (int j = 0; j < c2; j++) {
                for (int k = 0; k < c1/4 * 4; k+= 4){
                    result_data[i * c0 + j] += mat1_data[i * c1 + k] * mat2_data[k * c2 + j];
                    result_data[i * c0 + j] += mat1_data[i * c1 + k + 1] * mat2_data[(k+1) * c2 + j];
                    result_data[i * c0 + j] += mat1_data[i * c1 + k + 2] * mat2_data[(k+2) * c2 + j];
                    result_data[i * c0 + j] += mat1_data[i * c1 + k + 3] * mat2_data[(k+3) * c2 + j];
                }
                for (int t = c1/4*4; t < c1; t++){
                    result_data[i * c0 + j] += mat1_data[i * c1 + t] * mat2_data[t * c2 + j];
                }
            }
        }
    } else if (r1 * c2 < 10000) { // 24-99
        int i, j, k, t;
        #pragma omp parallel for private(i, j, k, t)
                for (i = 0; i < r1; i++) { 
                    for (j = 0; j < c2; j++) {
                        __m256d num0 = _mm256_set1_pd(0.0);
                        __m256d num1 = _mm256_set1_pd(0.0);
                        __m256d num2 = _mm256_set1_pd(0.0);
                        __m256d num3 = _mm256_set1_pd(0.0);
                        for (k = 0; k < c1/4 * 4; k+=4) {
                            __m256d m01 = _mm256_loadu_pd((double *) mat1_data + (i * c1 + k));
                            __m256d m02 = _mm256_loadu_pd((double *) mat2_data + (k * c2 + j));
                            
                            __m256d m11 = _mm256_loadu_pd((double *) mat1_data + (i * c1 + k + 1));
                            __m256d m12 = _mm256_loadu_pd((double *) mat2_data + ((k+1) * c2 + j));
                            
                            __m256d m21 = _mm256_loadu_pd((double *) mat1_data + (i * c1 + k + 2));
                            __m256d m22 = _mm256_loadu_pd((double *) mat2_data + ((k+2) * c2 + j));

                            __m256d m31 = _mm256_loadu_pd((double *) mat1_data + (i * c1 + k + 3));
                            __m256d m32 = _mm256_loadu_pd((double *) mat2_data + ((k+3) * c2 + j));

                            num0 = _mm256_fmadd_pd(m01, m02, num0);
                            num1 = _mm256_fmadd_pd(m11, m12, num1);
                            num2 = _mm256_fmadd_pd(m21, m22, num2);
                            num3 = _mm256_fmadd_pd(m31, m32, num3);
                        }
                        result_data[i * c0 + j] = num0[0] + num1[0] + num2[0] + num3[0];
                        for (t = c1/4 * 4; t < c1; t++) {
                            __m256d t1 = _mm256_loadu_pd((double *) mat1_data + (i * c1 + t));
                            __m256d t2 = _mm256_loadu_pd((double *) mat2_data + (t * c2 + j));
                            result_data[i * c0 + j] += _mm256_mul_pd(t1, t2)[0];
                        }
                    }
                }
    } else { // 100 or over
        double *matT = (double *)calloc(r2 * c2, sizeof(double));
        int i, j, t;
        #pragma omp parallel for private(i, j, t)
            for (i = 0; i < r2; i++) {
                for (j = 0; j < c2/4 * 4 ; j += 4) {
                    matT[j * r2 + i] = mat2_data[i * c2 + j];
                    matT[(j+1) * r2 + i] = mat2_data[i * c2 + (j+1)];
                    matT[(j+2) * r2 + i] = mat2_data[i * c2 + (j+2)];
                    matT[(j+3) * r2 + i] = mat2_data[i * c2 + (j+3)];
                }
                for (t = c2/4 * 4; t < c2; t++) {
                    matT[t * r2 + i] = mat2_data[i * c2 + t];
                }
            }
        #pragma omp parallel for private(i, j, t)
            for (i = 0; i < r1 * c2; i++) { 
                __m256d num01 = _mm256_set1_pd(0.0);
                __m256d num11 = _mm256_set1_pd(0.0);
                __m256d num21 = _mm256_set1_pd(0.0);
                __m256d num31 = _mm256_set1_pd(0.0);
                for (j = 0; j < r2/16*16 ; j+=16) {
                    __m256d m011 = _mm256_loadu_pd((double *) mat1_data + (i/c2 * c1 + j));
                    __m256d m021 = _mm256_loadu_pd((double *) matT + (i%c2 * r2 + j));

                    __m256d m111 = _mm256_loadu_pd((double *) mat1_data + (i/c2 * c1 + j + 4));
                    __m256d m121 = _mm256_loadu_pd((double *) matT + (i%c2 * r2 + j + 4));

                    __m256d m211 = _mm256_loadu_pd((double *) mat1_data + (i/c2 * c1 + j + 8));
                    __m256d m221 = _mm256_loadu_pd((double *) matT + (i%c2 * r2 + j + 8));

                    __m256d m311 = _mm256_loadu_pd((double *) mat1_data + (i/c2 * c1 + j + 12));
                    __m256d m321 = _mm256_loadu_pd((double *) matT + (i%c2 * r2 + j + 12));

                    num01 = _mm256_fmadd_pd(m011, m021, num01);
                    num11 = _mm256_fmadd_pd(m111, m121, num11);
                    num21 = _mm256_fmadd_pd(m211, m221, num21);
                    num31 = _mm256_fmadd_pd(m311, m321, num31);
                }
                result_data[i] = num01[0] + num01[1] + num01[2] + num01[3] + num11[0] + num11[1] + num11[2] + num11[3] 
                    + num21[0] + num21[1] + num21[2] + num21[3] + num31[0] + num31[1] + num31[2] + num31[3];

                for (t = r2/16*16; t < r2; t++) {
                    __m256d t1 = _mm256_loadu_pd((double *) mat1_data + (i/c2 * c1 + t));
                    __m256d t2 = _mm256_loadu_pd((double *) matT + (i%c2 * r2 + t));
                    result_data[i] += _mm256_mul_pd(t1, t2)[0];
                }
            }
        free(matT);
    }
    // fprintf(stdout, "Matrix Multiplication\n");
    // printmat(mat1);
    // printmat(mat2);
    // printmat(result);
    // fprintf(stdout, "Matrix Multiplication End \n");
    return 0;
}

/*
 * Store the result of raising mat to the (pow)th power to `result`.
 * Return 0 upon success and a nonzero value upon failure.
 * Remember that pow is defined with matrix multiplication, not element-wise multiplication.
 */
 int pow_matrix(matrix *result, matrix *mat, int pow) {        
    if (pow == 1) {
            for (int i = 0; i < mat->rows; i++) {
                for (int j = 0; j < mat->cols/4*4; j+=4) {
                    result->data[i * mat->cols + j] = mat->data[i * mat->cols + j];
                    result->data[i * mat->cols + j + 1] = mat->data[i * mat->cols + j + 1];
                    result->data[i * mat->cols + j + 2] = mat->data[i * mat->cols + j + 2];
                    result->data[i * mat->cols + j + 3] = mat->data[i * mat->cols + j + 3];
                }
                for (int t = mat->cols/4*4; t < mat->cols; t++) {
                    result->data[i * result->cols + t] = mat->data[i * mat->cols + t];
                }
            }
        return 0;
    } else if (pow == 0) {
        for (int i = 0; i < result->rows; i++) {
            result->data[i * result->cols + i] = 1;
        }
        return 0;
    }
    #pragma omp parallel for 
        for (int i = 0; i < result->rows; i++) {
            result->data[i * result->cols + i] = 1;
        }

    matrix *dupe;
    allocate_matrix(&dupe, mat->rows, mat->cols);
    matrix *save;
    allocate_matrix(&save, mat->rows, mat->cols);
    int i, j, t;
    //#pragma omp parallel for private(i, j, t)
        for (i = 0; i < mat->rows; i++) {
            for (j = 0; j < mat->cols/4*4; j+=4) {
                dupe->data[i * mat->cols + j] = mat->data[i * mat->cols + j];
                dupe->data[i * mat->cols + j + 1] = mat->data[i * mat->cols + j + 1];
                dupe->data[i * mat->cols + j + 2] = mat->data[i * mat->cols + j + 2];
                dupe->data[i * mat->cols + j + 3] = mat->data[i * mat->cols + j + 3];
            }
            for (t = mat->cols/4*4; t < mat->cols; t++) {
                dupe->data[i * mat->cols + t] = mat->data[i * mat->cols + t];
            }
        }
    matrix *resultsave = result;

    matrix *pointerdupe = dupe;
    matrix *pointersave = save;
    while (pow > 0) {
        if (pow & 1) {
            mulpow(save, result, dupe);
            matrix *temp = result;
            result = save;
            save = temp;
        } 
        mulpow(save, dupe, dupe);
        matrix *temp = dupe;
        dupe = save;
        save = temp;
        pow = pow/2;
    }
    if (result != resultsave) {
        //#pragma omp parallel for private(i, j, t)
        for (i = 0; i < result->rows; i++) {
            for (j = 0; j < result->cols/4*4; j+=4) {
                resultsave->data[i * result->cols + j] = result->data[i * result->cols + j];
                resultsave->data[i * result->cols + j + 1] = result->data[i * result->cols + j + 1];
                resultsave->data[i * result->cols + j + 2] = result->data[i * result->cols + j + 2];
                resultsave->data[i * result->cols + j + 3] = result->data[i * result->cols + j + 3];
            }
            for (t = result->cols/4*4; t < result->cols; t++) {
                resultsave->data[i * result->cols + t] = result->data[i * result->cols + t];
            }
        }
    }
    deallocate_matrix(pointerdupe);
    deallocate_matrix(pointersave);
    return 0;
}

void mulpow(matrix *result, matrix *mat1, matrix *mat2) {
    int r1 = mat1->rows;
    int c1 = mat1->cols;
    int r2 = mat2->rows;
    int c2 = mat2->cols;
    int c0 = result->cols;
    double *mat1_data = mat1->data;
    double *mat2_data = mat2->data;
    double *result_data = result->data;
    if (r1 * c2 < 1000) {
        double num;
        for (int i = 0; i < r1; i++) {
            for (int j = 0; j < c2; j++) {
                for (int k = 0; k < c1; k++){
                    num += mat1_data[i * c1 + k] * mat2_data[k * c2 + j];
                }
                result_data[i * c0 + j] = num;
                num = 0.0;
            }
    }
    } else if (r1 * c2 < 7000) {
        int i, j, k, t;
        #pragma omp parallel for private(i, j, k, t)
                for (i = 0; i < r1; i++) { 
                    for (j = 0; j < c2; j++) {
                        __m256d num0 = _mm256_set1_pd(0.0);
                        __m256d num1 = _mm256_set1_pd(0.0);
                        __m256d num2 = _mm256_set1_pd(0.0);
                        __m256d num3 = _mm256_set1_pd(0.0);
                        for (k = 0; k < c1/4 * 4; k+=4) {
                            __m256d m01 = _mm256_loadu_pd((double *) mat1_data + (i * c1 + k));
                            __m256d m02 = _mm256_loadu_pd((double *) mat2_data + (k * c2 + j));
                            
                            __m256d m11 = _mm256_loadu_pd((double *) mat1_data + (i * c1 + k + 1));
                            __m256d m12 = _mm256_loadu_pd((double *) mat2_data + ((k+1) * c2 + j));
                            
                            __m256d m21 = _mm256_loadu_pd((double *) mat1_data + (i * c1 + k + 2));
                            __m256d m22 = _mm256_loadu_pd((double *) mat2_data + ((k+2) * c2 + j));

                            __m256d m31 = _mm256_loadu_pd((double *) mat1_data + (i * c1 + k + 3));
                            __m256d m32 = _mm256_loadu_pd((double *) mat2_data + ((k+3) * c2 + j));

                            num0 = _mm256_fmadd_pd(m01, m02, num0);
                            num1 = _mm256_fmadd_pd(m11, m12, num1);
                            num2 = _mm256_fmadd_pd(m21, m22, num2);
                            num3 = _mm256_fmadd_pd(m31, m32, num3);
                        }
                        result_data[i * c0 + j] = num0[0] + num1[0] + num2[0] + num3[0];
                        for (t = c1/4 * 4; t < c1; t++) {
                            __m256d t1 = _mm256_loadu_pd((double *) mat1_data + (i * c1 + t));
                            __m256d t2 = _mm256_loadu_pd((double *) mat2_data + (t * c2 + j));
                            result_data[i * c0 + j] += _mm256_mul_pd(t1, t2)[0];
                        }
                    }
                }
    } else {
        double *matT = (double *)calloc(r2 * c2, sizeof(double));
        int i, j, t;
        #pragma omp parallel for private(i, j, t)
            for (i = 0; i < r2; i++) {
                for (j = 0; j < c2/4 * 4 ; j += 4) {
                    matT[j * r2 + i] = mat2_data[i * c2 + j];
                    matT[(j+1) * r2 + i] = mat2_data[i * c2 + (j+1)];
                    matT[(j+2) * r2 + i] = mat2_data[i * c2 + (j+2)];
                    matT[(j+3) * r2 + i] = mat2_data[i * c2 + (j+3)];
                }
                for (t = c2/4 * 4; t < c2; t++) {
                    matT[t * r2 + i] = mat2_data[i * c2 + t];
                }
            }
        #pragma omp parallel for private(i, j, t)
            for (i = 0; i < r1 * c2; i++) { 
                __m256d num01 = _mm256_set1_pd(0.0);
                __m256d num11 = _mm256_set1_pd(0.0);
                __m256d num21 = _mm256_set1_pd(0.0);
                __m256d num31 = _mm256_set1_pd(0.0);
                for (j = 0; j < r2/16*16 ; j+=16) {
                    __m256d m011 = _mm256_loadu_pd((double *) mat1_data + (i/c2 * c1 + j));
                    __m256d m021 = _mm256_loadu_pd((double *) matT + (i%c2 * r2 + j));

                    __m256d m111 = _mm256_loadu_pd((double *) mat1_data + (i/c2 * c1 + j + 4));
                    __m256d m121 = _mm256_loadu_pd((double *) matT + (i%c2 * r2 + j + 4));

                    __m256d m211 = _mm256_loadu_pd((double *) mat1_data + (i/c2 * c1 + j + 8));
                    __m256d m221 = _mm256_loadu_pd((double *) matT + (i%c2 * r2 + j + 8));

                    __m256d m311 = _mm256_loadu_pd((double *) mat1_data + (i/c2 * c1 + j + 12));
                    __m256d m321 = _mm256_loadu_pd((double *) matT + (i%c2 * r2 + j + 12));

                    num01 = _mm256_fmadd_pd(m011, m021, num01);
                    num11 = _mm256_fmadd_pd(m111, m121, num11);
                    num21 = _mm256_fmadd_pd(m211, m221, num21);
                    num31 = _mm256_fmadd_pd(m311, m321, num31);
                }
                result_data[i] = num01[0] + num01[1] + num01[2] + num01[3] + num11[0] + num11[1] + num11[2] + num11[3] 
                    + num21[0] + num21[1] + num21[2] + num21[3] + num31[0] + num31[1] + num31[2] + num31[3];

                for (t = r2/16*16; t < r2; t++) {
                    __m256d t1 = _mm256_loadu_pd((double *) mat1_data + (i/c2 * c1 + t));
                    __m256d t2 = _mm256_loadu_pd((double *) matT + (i%c2 * r2 + t));
                    result_data[i] += _mm256_mul_pd(t1, t2)[0];
                }
            }
        free(matT);
    }
    }

/*
 * Store the result of element-wise negating mat's entries to `result`.
 * Return 0 upon success and a nonzero value upon failure.
 */
int neg_matrix(matrix *result, matrix *mat) {
    int i, j, t;
    #pragma omp parallel for private(i, j, t)
        for (i = 0; i < mat->rows; i++) {
            for (j = 0; j < mat->cols/4*4; j+=4) {
                result->data[i * result->cols + j] = -mat->data[i * mat->cols + j];
                result->data[i * result->cols + j+1] = -mat->data[i * mat->cols + j+1];
                result->data[i * result->cols + j+2] = -mat->data[i * mat->cols + j+2];
                result->data[i * result->cols + j+3] = -mat->data[i * mat->cols + j+3];
            }
            for (t = mat->cols/4*4; t < mat->cols; t++) {
                result->data[i * result->cols + t] = -mat->data[i * mat->cols + t];
            }
        }
    return 0;
}

/*
 * Store the result of taking the absolute value element-wise to `result`.
 * Return 0 upon success and a nonzero value upon failure.
 */
int abs_matrix(matrix *result, matrix *mat) {
    int i, j, t;
    #pragma omp parallel for private(i, j, t)
        for (i = 0; i < mat->rows; i++) {
             for (j = 0; j < mat->cols/4*4; j+=4) {
                result->data[i * result->cols + j] = fabs(mat->data[i * mat->cols + j]);
                result->data[i * result->cols + j+1] = fabs(mat->data[i * mat->cols + j + 1]);
                result->data[i * result->cols + j+2] = fabs(mat->data[i * mat->cols + j + 2]);
                result->data[i * result->cols + j+3] = fabs(mat->data[i * mat->cols + j + 3]);
            }
            for (t = mat->cols/4*4; t < mat->cols; t++) {
                result->data[i * result->cols + t] = fabs(mat->data[i * mat->cols + t]);
            }
        }
    return 0;
}

void mcopy(matrix *result, matrix *mat, int rows, int cols) {
    int i, j, t;
    #pragma omp parallel for private(i, j, t)
        for (i = 0; i < rows; i++) {
            for (j = 0; j < cols/4*4; j+=4) {
                result->data[i * cols + j] = mat->data[i * cols + j];
                result->data[i * cols + j + 1] = mat->data[i * cols + j + 1];
                result->data[i * cols + j + 2] = mat->data[i * cols + j + 2];
                result->data[i * cols + j + 3] = mat->data[i * cols + j + 3];
            }
            for (t = cols/4*4; t < cols; t++) {
                result->data[i * cols + t] = mat->data[i * cols + t];
            }
        }
}

void printmat(matrix *mat) {
    fprintf(stdout, "\n");
    for (int i = 0; i < mat->rows; i++) {
        for (int j = 0; j < mat->cols; j++) {
            printf("%f ", get(mat, i, j));
        }
        fprintf(stdout, "\n");
    }
    fprintf(stdout, "\n");
}

// #pragma omp parallel for private(i, j, t)
            //     for (i = 0; i < save->rows; i++) {
            //         for (j = 0; j < save->cols/4*4; j+=4) {
            //             result->data[i * save->cols + j] = save->data[i * save->cols + j];
            //             result->data[i * save->cols + j + 1] = save->data[i * save->cols + j + 1];
            //             result->data[i * save->cols + j + 2] = save->data[i * save->cols + j + 2];
            //             result->data[i * save->cols + j + 3] = save->data[i * save->cols + j + 3];
            //         }
            //         for (t = save->cols/4*4; t < save->cols; t++) {
            //             result->data[i * save->cols + t] = save->data[i * save->cols + t];
            //         }
            //     }

// #pragma omp parallel for private(i, j, t)
        //     for (i = 0; i < save->rows; i++) {
        //         for (j = 0; j < save->cols/4*4; j+=4) {
        //                 dupe->data[i * save->cols + j] = save->data[i * save->cols + j];
        //                 dupe->data[i * save->cols + j + 1] = save->data[i * save->cols + j + 1];
        //                 dupe->data[i * save->cols + j + 2] = save->data[i * save->cols + j + 2];
        //                 dupe->data[i * save->cols + j + 3] = save->data[i * save->cols + j + 3];
        //             }
        //         for (t = save->cols/4*4; t < save->cols; t++) {
        //             dupe->data[i * save->cols + t] = save->data[i * save->cols + t];
        //         }
        //     }
