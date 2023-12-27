from utils import *
from unittest import TestCase

"""
- For each operation, you should write tests to test on matrices of different sizes.
- Keep in mind that the tests provided in the starter code are NOT comprehensive. That is, we strongly
advise you to modify them and add new tests.
- Hint: use dp_mc_matrix to generate dumbpy and numc matrices with the same data and use
      cmp_dp_nc_matrix to compare the results
"""
class TestAdd(TestCase):
    def test_small_add(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(2, 2, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(2, 2, seed=1)
        is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "add")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_medium_add(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(500, 500, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(500, 500, seed=1)
        is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "add")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_large_add(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(12000, 12000, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(12000, 12000, seed=1)
        is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "add")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_add_ValueError(self):
        try:
            nc.Matrix(3, 3) + nc.Matrix(2, 2)
            self.assertTrue(False)
        except ValueError as e:
            pass

class TestSub(TestCase):
    def test_small_sub(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(2, 2, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(2, 2, seed=1)
        is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "sub")
        self.assertTrue(is_correct)
        try:
            nc.Matrix(3, 3) - nc.Matrix(2, 2)
            self.assertTrue(False)
        except ValueError as e:
            #print(e)
            pass
        print_speedup(speed_up)

    def test_medium_sub(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(500, 500, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(500, 500, seed=1)
        is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "sub")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_large_sub(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(12000, 12000, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(12000, 12000, seed=1)
        is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "sub")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

class TestAbs(TestCase):
    def test_small_abs(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(2, 2, seed=0)
        is_correct, speed_up = compute([dp_mat], [nc_mat], "abs")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_medium_abs(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(500, 500, seed=0)
        is_correct, speed_up = compute([dp_mat], [nc_mat], "abs")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_large_abs(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(12000, 12000, seed=0)
        is_correct, speed_up = compute([dp_mat], [nc_mat], "abs")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

class TestNeg(TestCase):
    def test_small_neg(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(2, 2, seed=0)
        is_correct, speed_up = compute([dp_mat], [nc_mat], "neg")
        self.assertTrue(is_correct)
        print_speedup(speed_up)
    def test_medium_neg(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(500, 500, seed=0)
        is_correct, speed_up = compute([dp_mat], [nc_mat], "neg")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_large_neg(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(12000, 12000, seed=0)
        is_correct, speed_up = compute([dp_mat], [nc_mat], "neg")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

class TestMul(TestCase):

    def test_mul_ValueError(self):
        try:
            nc.Matrix(3, 3) * nc.Matrix(2, 3)
            self.assertTrue(False)
        except ValueError as e:
            pass
    
    def test_small_mul(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(2, 2, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(2, 2, seed=1)
        is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "mul")
        self.assertTrue(is_correct)
        print_speedup(speed_up)
    
    def test_medium_mul(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(600, 600, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(600, 600, seed=1)
        is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "mul")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_large_mul(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(1200, 1200, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(1200, 1200, seed=1)
        is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "mul")
        self.assertTrue(is_correct)
        print_speedup(speed_up)
    
    def test_mul01(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(4, 5, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(5, 3, seed=1)
        is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "mul")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_mul02(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(15, 17, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(17, 20, seed=1)
        is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "mul")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_mul025(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(25, 25, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(25, 25, seed=1)
        is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "mul")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_mul050(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(50, 50, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(50, 50, seed=1)
        is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "mul")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_mul100(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(100, 100, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(100, 100, seed=1)
        is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "mul")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_mul200(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(200, 200, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(200, 200, seed=1)
        is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "mul")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_mul300(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(300, 300, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(300, 300, seed=1)
        is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "mul")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_mul400(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(400, 400, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(400, 400, seed=1)
        is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "mul")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_mul600(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(600, 600, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(600, 600, seed=1)
        is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "mul")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_mul800(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(800, 800, seed=0)
        dp_mat2, nc_mat2 = rand_dp_nc_matrix(800, 800, seed=1)
        is_correct, speed_up = compute([dp_mat1, dp_mat2], [nc_mat1, nc_mat2], "mul")
        self.assertTrue(is_correct)
        print_speedup(speed_up)


class TestPow(TestCase):
    """
    def test_pow_TypeError(self):
        try:
            nc.Matrix(3, 3) ** 1.2
            self.assertTrue(False)
        except TypeError as e:
            pass

    def test_pow_ValueError0(self):
        try:
            nc.Matrix(3, 3) ** -2
            self.assertTrue(False)
        except ValueError as e:
            pass

    def test_pow_ValueError1(self):
        try:
            nc.Matrix(3, 2) ** 2
            self.assertTrue(False)
        except ValueError as e:
            pass
    """
    def test_powId(self):
        dp_mat0, nc_mat0 = rand_dp_nc_matrix(10, 10, seed=0)
        is_correct, speed_up = compute([dp_mat0, 0], [nc_mat0, 0], "pow")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_pow(self):
        dp_mat1, nc_mat1 = rand_dp_nc_matrix(10, 10, seed=0)
        is_correct, speed_up = compute([dp_mat1, 1], [nc_mat1, 1], "pow")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_pow007(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(7, 7, seed=0)
        is_correct, speed_up = compute([dp_mat, 3], [nc_mat, 3], "pow")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_pow010(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(10, 10, seed=0)
        is_correct, speed_up = compute([dp_mat, 50], [nc_mat, 50], "pow")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_pow035(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(35, 35, seed=0)
        is_correct, speed_up = compute([dp_mat, 250], [nc_mat, 250], "pow")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_pow060(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(60, 60, seed=0)
        is_correct, speed_up = compute([dp_mat, 500], [nc_mat, 500], "pow")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_pow090(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(90, 90, seed=0)
        is_correct, speed_up = compute([dp_mat, 750], [nc_mat, 750], "pow")
        self.assertTrue(is_correct)
        print_speedup(speed_up)

    def test_pow120(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(120, 120, seed=0)
        is_correct, speed_up = compute([dp_mat, 1000], [nc_mat, 1000], "pow")
        self.assertTrue(is_correct)
        print_speedup(speed_up)


class TestGet(TestCase):
    def test_get(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(2, 2, seed=0)
        rand_row = np.random.randint(dp_mat.shape[0])
        rand_col = np.random.randint(dp_mat.shape[1])
        self.assertEqual(round(dp_mat.get(rand_row, rand_col), decimal_places),
            round(nc_mat.get(rand_row, rand_col), decimal_places))

class TestSet(TestCase):
    def test_set(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(2, 2, seed=0)
        rand_row = np.random.randint(dp_mat.shape[0])
        rand_col = np.random.randint(dp_mat.shape[1])
        dp_mat.set(rand_row, rand_col, 2)
        nc_mat.set(rand_row, rand_col, 2)
        self.assertTrue(cmp_dp_nc_matrix(dp_mat, nc_mat))

        dp_mat1, nc_mat1 = rand_dp_nc_matrix(5, 7, seed=0)
        rand_row1 = np.random.randint(dp_mat1.shape[0])
        rand_col1 = np.random.randint(dp_mat1.shape[1])
        dp_mat1.set(rand_row1, rand_col1, 6.0)
        nc_mat1.set(rand_row1, rand_col1, 6.0)
        self.assertTrue(cmp_dp_nc_matrix(dp_mat1, nc_mat1))

class TestShape(TestCase):
    def test_shape(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(2, 2, seed=0)
        self.assertTrue(dp_mat.shape == nc_mat.shape)

class TestIndexGet(TestCase):
    def test_index_get(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(2, 2, seed=0)
        rand_row = np.random.randint(dp_mat.shape[0])
        rand_col = np.random.randint(dp_mat.shape[1])
        self.assertEqual(round(dp_mat[rand_row][rand_col], decimal_places),
            round(nc_mat[rand_row][rand_col], decimal_places))

class TestIndexSet(TestCase):
    def test_set(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(2, 2, seed=0)
        rand_row = np.random.randint(dp_mat.shape[0])
        rand_col = np.random.randint(dp_mat.shape[1])
        dp_mat[rand_row][rand_col] = 2
        nc_mat[rand_row][rand_col] = 2
        self.assertTrue(cmp_dp_nc_matrix(dp_mat, nc_mat))
        self.assertEqual(nc_mat[rand_row][rand_col], 2)

class TestSlice(TestCase):
    def test_slice(self):
        dp_mat, nc_mat = rand_dp_nc_matrix(2, 2, seed=0)
        self.assertTrue(cmp_dp_nc_matrix(dp_mat[0], nc_mat[0]))
        self.assertTrue(cmp_dp_nc_matrix(dp_mat[1], nc_mat[1]))
