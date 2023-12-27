from unittest import TestCase
from framework import AssemblyTest, print_coverage


class TestAbs(TestCase):

    def test_zero(self):
        t = AssemblyTest(self, "abs.s")
        # load 0 into register a0
        t.input_scalar("a0", 0)
        # call the abs function
        t.call("abs")
        # check that after calling abs, a0 is equal to 0 (abs(0) = 0)
        t.check_scalar("a0", 0)
        # generate the `assembly/TestAbs_test_zero.s` file and run it through venus
        t.execute()

    def test_one(self):
        # same as test_zero, but with input 1
        t = AssemblyTest(self, "abs.s")
        t.input_scalar("a0", 1)
        t.call("abs")
        t.check_scalar("a0", 1)
        t.execute()
    
    def test_minus_one(self):
    	t = AssemblyTest(self, "abs.s")
    	t.input_scalar("a0", -1)
    	t.call("abs")
    	t.check_scalar("a0", 1)
    	t.execute()
    
    def test_minus_one(self):
    	t = AssemblyTest(self, "abs.s")
    	t.input_scalar("a0", -1)
    	t.call("abs")
    	t.check_scalar("a0", 1)
    	t.execute()

    @classmethod
    def tearDownClass(cls):
        print_coverage("abs.s", verbose=False)

class TestRelu(TestCase):
    def test_simple(self):
        t = AssemblyTest(self, "relu.s")
        # create an array in the data section
        array0 = t.array([1, -2, 3, -4, 5, -6, 7, -8, 9])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the relu function
        t.call("relu")
        # check that the array0 was changed appropriately
        t.check_array(array0, [1, 0, 3, 0, 5, 0, 7, 0, 9])
        # generate the `assembly/TestRelu_test_simple.s` file and run it through venus
        t.execute()
        
    def test_one_element(self):
        t = AssemblyTest(self, "relu.s")
        # create an array in the data section
        array0 = t.array([-2])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the relu function
        t.call("relu")
        # check that the array0 was changed appropriately
        t.check_array(array0, [0])
        # generate the `assembly/TestRelu_test_simple.s` file and run it through venus
        t.execute()
        
    def test_empty(self):
        t = AssemblyTest(self, "relu.s")
        # create an array in the data section
        array0 = t.array([])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the relu function
        t.call("relu")
        # generate the `assembly/TestRelu_test_simple.s` file and run it through venus
        t.execute(code=115)

    def test_1(self):
        t = AssemblyTest(self, "relu.s")
        # create an array in the data section
        array0 = t.array([54])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the relu function
        t.call("relu")
        # check that the array0 was changed appropriately
        t.check_array(array0, [54])
        # generate the `assembly/TestRelu_test_simple.s` file and run it through venus
        t.execute()

    def test_2(self):
        t = AssemblyTest(self, "relu.s")
        # create an array in the data section
        array0 = t.array([0])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the relu function
        t.call("relu")
        # check that the array0 was changed appropriately
        t.check_array(array0, [0])
        # generate the `assembly/TestRelu_test_simple.s` file and run it through venus
        t.execute()
        

    @classmethod
    def tearDownClass(cls):
        print_coverage("relu.s", verbose=False)


class TestArgmax(TestCase):
    def test_simple(self):
        t = AssemblyTest(self, "argmax.s")
        # create an array in the data section
        array0 = t.array([1, -2, 100, -4, 5, -6, 7, -8, 9])
        # load address of the array into register a0
        t.input_array("a0", array0)
        # set a1 to the length of the array
        t.input_scalar("a1", len(array0))
        # call the `argmax` function
        t.call("argmax")
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 2)
        # generate the `assembly/TestArgmax_test_simple.s` file and run it through venus
        t.execute()
        
    def test_empty(self):
        t = AssemblyTest(self, "argmax.s")
        # create an array in the data section
        array0 = t.array([])
        # load address of the array into register a0
        t.input_array("a0", array0)
        # set a1 to the length of the array
        t.input_scalar("a1", len(array0))
        # call the `argmax` function
        t.call("argmax")
        # generate the `assembly/TestArgmax_test_simple.s` file and run it through venus
        t.execute(code=120)

    def test_one_element(self):
        t = AssemblyTest(self, "argmax.s")
        # create an array in the data section
        array0 = t.array([-2])
        # load address of the array into register a0
        t.input_array("a0", array0)
        # set a1 to the length of the array
        t.input_scalar("a1", len(array0))
        # call the `argmax` function
        t.call("argmax")
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 0)
        # generate the `assembly/TestArgmax_test_simple.s` file and run it through venus
        t.execute()

    def test_1(self):
        t = AssemblyTest(self, "argmax.s")
        # create an array in the data section
        array0 = t.array([0, 1, 3, 1, 5])
        # load address of the array into register a0
        t.input_array("a0", array0)
        # set a1 to the length of the array
        t.input_scalar("a1", len(array0))
        # call the `argmax` function
        t.call("argmax")
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 4)
        # generate the `assembly/TestArgmax_test_simple.s` file and run it through venus
        t.execute()

    def test_2(self):
        t = AssemblyTest(self, "argmax.s")
        # create an array in the data section
        array0 = t.array([-1000, 2000])
        # load address of the array into register a0
        t.input_array("a0", array0)
        # set a1 to the length of the array
        t.input_scalar("a1", len(array0))
        # call the `argmax` function
        t.call("argmax")
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 1)
        # generate the `assembly/TestArgmax_test_simple.s` file and run it through venus
        t.execute()
        

    @classmethod
    def tearDownClass(cls):
        print_coverage("argmax.s", verbose=False)


class TestDot(TestCase):
    def test_simple(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        array1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        # load array attributes into argument registers
        t.input_array("a1", array1)
        t.input_scalar("a2", len(array0))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.check_scalar("a0", 285)
        t.execute()

    def test_empty_vector(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array0 = t.array([])
        array1 = t.array([])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        # load array attributes into argument registers
        t.input_array("a1", array1)
        t.input_scalar("a2", len(array0))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.execute(code=123)

    def test_empty_stride(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array0 = t.array([1, 2, 3, 4, 5, 6])
        array1 = t.array([1, 2, 3, 4, 5, 6])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        # load array attributes into argument registers
        t.input_array("a1", array1)
        t.input_scalar("a2", len(array0))
        t.input_scalar("a3", -1)
        t.input_scalar("a4", -1)
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.execute(code=124)

    def test_empty_both(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array0 = t.array([])
        array1 = t.array([])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        # load array attributes into argument registers
        t.input_array("a1", array1)
        t.input_scalar("a2", len(array0))
        t.input_scalar("a3", -1)
        t.input_scalar("a4", -1)
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.execute(code=123)

    def test_one_element(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array0 = t.array([9])
        array1 = t.array([6])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        # load array attributes into argument registers
        t.input_array("a1", array1)
        t.input_scalar("a2", len(array0))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.check_scalar("a0", 54)
        t.execute()

    def test_stride(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        array1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        # load array attributes into argument registers
        t.input_array("a1", array1)
        t.input_scalar("a2", 3)
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 2)
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.check_scalar("a0", 22)
        t.execute()

    def test_2_stride(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array0 = t.array([1, 2, 3, 4, 5])
        array1 = t.array([1, 2, 3, 4, 5])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        # load array attributes into argument registers
        t.input_array("a1", array1)
        t.input_scalar("a2", 3)
        t.input_scalar("a3", 2)
        t.input_scalar("a4", 2)
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.check_scalar("a0", 35)
        t.execute()
    
    def test_big_stride(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array0 = t.array([1, 2, 3, 4, 5])
        array1 = t.array([1, 2, 3, 4, 5])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        # load array attributes into argument registers
        t.input_array("a1", array1)
        t.input_scalar("a2", 1)
        t.input_scalar("a3", 10)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.check_scalar("a0", 1)
        t.execute()

    def test_diff_len_vector(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        array1 = t.array([1, 2, 3, 4, 5])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        # load array attributes into argument registers
        t.input_array("a1", array1)
        t.input_scalar("a2", 5)
        t.input_scalar("a3", 2)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.check_scalar("a0", 95)
        t.execute()

    def test_zero(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array0 = t.array([0, 0, 0, 0, 0, 6, 0, 8, 0])
        array1 = t.array([1, 2, 3, 4, 5])
        # load array addresses into argument registers
        t.input_array("a0", array0)
        # load array attributes into argument registers
        t.input_array("a1", array1)
        t.input_scalar("a2", 5)
        t.input_scalar("a3", 2)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.check_scalar("a0", 0)
        t.execute()

    @classmethod
    def tearDownClass(cls):
        print_coverage("dot.s", verbose=False)


class TestMatmul(TestCase):

    def do_matmul(self, m0, m0_rows, m0_cols, m1, m1_rows, m1_cols, result, code=0):
        t = AssemblyTest(self, "matmul.s")
        # we need to include (aka import) the dot.s file since it is used by matmul.s
        t.include("dot.s")

        # create arrays for the arguments and to store the result
        array0 = t.array(m0)
        array1 = t.array(m1)
        array_out = t.array([0] * len(result))

        # load address of input matrices and set their dimensions
        t.input_array("a0", array0)
        t.input_scalar("a1", m0_rows)
        t.input_scalar("a2", m0_cols)
        t.input_array("a3", array1)
        t.input_scalar("a4", m1_rows)
        t.input_scalar("a5", m1_cols)
        # load address of output array
        t.input_array("a6", array_out)
        # call the matmul function
        t.call("matmul")
        # check the content of the output array
        t.check_array(array_out, result)
        # generate the assembly file and run it through venus, we expect the simulation to exit with code `code`
        t.execute(code=code)

    def test_simple(self):
        self.do_matmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [30, 36, 42, 66, 81, 96, 102, 126, 150]
        )

    def test_empty_m0(self):
        self.do_matmul(
            [], 0, 0,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [30, 36, 42, 66, 81, 96, 102, 126, 150], 125
        )

    def test_empty_m1(self):
        self.do_matmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [], 0, 0,
            [30, 36, 42, 66, 81, 96, 102, 126, 150], 126
        )

    def test_empty_both(self):
        self.do_matmul(
            [], 0, 0,
            [], 0, 0,
            [30, 36, 42, 66, 81, 96, 102, 126, 150], 125
        )

    def test_mismatch(self):
        self.do_matmul(
            [1, 2, 3, 4, 5, 6], 2, 3,
            [1, 2, 3, 4, 5, 6], 2, 3,
            [30, 36, 42, 66, 81, 96, 102, 126, 150], 127
        )

    def test_23(self):
        self.do_matmul(
            [1, 2, 3, 4, 5, 6], 2, 3,
            [1, 2, 3, 4, 5, 6], 3, 2,
            [22, 28, 49, 64]
        )

    def test_110(self):
        self.do_matmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 1, 10,
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10, 1,
            [385]
        )

    def test_neg(self):
        self.do_matmul(
            [-1, 2, 3, -4, -5, 6, 7, 8, -9], 3, 3,
            [1, -2, 3, 4, -5, 6, -7, 8, 9], 3, 3,
            [-14, 16, 36, -66, 81, 12, 102, -126, -12]
        )

    def test_one_element(self):
        self.do_matmul(
            [4], 1, 1, 
            [3], 1, 1,
            [12]
        )

    def test_100(self):
        self.do_matmul(
            [7, 2, 3, 4, 5, 3, 7, 8, 9, 10], 10, 1,
            [1, 2, -6, 4, 5, 6, 7, 8, 0, 10], 1, 10,
            [7, 14, -42, 28, 35, 42, 49, 56, 0, 70, 
             2, 4, -12, 8, 10, 12, 14, 16, 0, 20, 
             3, 6, -18, 12, 15, 18, 21, 24, 0, 30, 
             4, 8, -24, 16, 20, 24, 28, 32, 0, 40,
             5, 10, -30, 20, 25, 30, 35, 40, 0, 50, 
             3, 6, -18, 12, 15, 18, 21, 24, 0, 30,
             7, 14, -42, 28, 35, 42, 49, 56, 0, 70, 
             8, 16, -48, 32, 40, 48, 56, 64, 0, 80,
             9, 18, -54, 36, 45, 54, 63, 72, 0, 90, 
             10, 20, -60, 40, 50, 60, 70, 80, 0, 100]
        )


    @classmethod
    def tearDownClass(cls):
        print_coverage("matmul.s", verbose=False)


class TestReadMatrix(TestCase):

    def do_read_matrix(self, filename, output, fail="", code=0):
        t = AssemblyTest(self, "read_matrix.s")
        # load address to the name of the input file into register a0
        t.input_read_filename("a0", filename)

        # allocate space to hold the rows and cols output parameters
        rows = t.array([-1])
        cols = t.array([-1])

        # load the addresses to the output parameters into the argument registers
        t.input_array("a1", rows)
        t.input_array("a2", cols)
        # TODO

        # call the read_matrix function
        t.call("read_matrix")

        # check the output from the function
        # TODO
        t.check_array_pointer("a0", output)
        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)

    def test_simple(self):
        self.do_read_matrix("inputs/test_read_matrix/test_input.bin", [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_malloc(self):
        self.do_read_matrix("inputs/test_read_matrix/test_input.bin", [1, 2, 3, 4, 5], 
            fail="malloc", code=116)

    def test_fopen(self):
        self.do_read_matrix("inputs/test_read_matrix/test_input.bin", [1, 2, 3, 4, 5],
            fail="fopen", code=117)

    def test_fread(self):
        self.do_read_matrix("inputs/test_read_matrix/test_input.bin", [1, 2, 3, 4, 5],
            fail="fread", code=118)

    def test_fclose(self):
        self.do_read_matrix("inputs/test_read_matrix/test_input.bin", [0, 1, 1],
            fail="fclose", code=119)

    def test_1(self):
        self.do_read_matrix("inputs/test_read_matrix/test1.bin", [8])

    def test_24(self):
        self.do_read_matrix("inputs/test_read_matrix/test24.bin", [1, 2, 3, 4, 5, 6, 7, 8])

    def test_neg(self):
        self.do_read_matrix("inputs/test_read_matrix/testneg.bin", [-1, -2, -3, -4, -5, -6, -7, -8])

    def test_big(self):
        self.do_read_matrix("inputs/test_read_matrix/testbig.bin",
          [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
          18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
          35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,
          52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68,
          69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85,
          86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100])

    def test_19(self):
        self.do_read_matrix("inputs/test_read_matrix/test19.bin", [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_91(self):
        self.do_read_matrix("inputs/test_read_matrix/test91.bin", [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_empty(self):
        self.do_read_matrix("inputs/test_read_matrix/testempty.bin", [1, 2, 3],
            fail="fread", code=118)

    #def test_none(self):
        #self.do_read_matrix("inputs/test_read_matrix/testnone.bin", [1, 2, 3],
            #fail="fopen", code=117)

    @classmethod
    def tearDownClass(cls):
        print_coverage("read_matrix.s", verbose=False)


class TestWriteMatrix(TestCase):

    def do_write_matrix(self, outfile, rows, cols, matrix, reference, fail='', code=0):
        t = AssemblyTest(self, "write_matrix.s")
        # load output file name into a0 register
        t.input_write_filename("a0", outfile)
        # load input array and other arguments
        t.input_array("a1", t.array(matrix))
        t.input_scalar("a2", rows)
        t.input_scalar("a3", cols)
        # TODO
        # call `write_matrix` function
        t.call("write_matrix")
        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)
        # compare the output file against the reference
        if (fail == ''):
            t.check_file_output(outfile, reference)

    def test_simple(self):
        self.do_write_matrix("outputs/test_write_matrix/student.bin", 
            3, 3, [1, 2, 3, 4, 5, 6, 7, 8, 9], "outputs/test_write_matrix/reference.bin")

    def test_fopen(self):
        self.do_write_matrix("", 1, 3, [1, 2, 3], "",
            fail="fopen", code=112)

    def test_fwrite(self):
        self.do_write_matrix("outputs/test_write_matrix/student.bin", 1, 3, [1, 2, 3], "",
            fail="fwrite", code=113)

    def test_fclose(self):
        self.do_write_matrix("outputs/test_write_matrix/student.bin", 1, 3, [1, 2, 3],"",
            fail="fclose", code=114)

    def test_24(self):
        self.do_write_matrix("outputs/test_write_matrix/24.bin", 
            2, 4, [1, 2, 3, 4, 5, 6, 7, 8], "outputs/test_write_matrix/24ref.bin")

    def test_1(self):
        self.do_write_matrix("outputs/test_write_matrix/test1.bin", 
            1, 1, [6], "outputs/test_write_matrix/test1ref.bin")

    def test_big(self):
        self.do_write_matrix("outputs/test_write_matrix/big.bin", 
            10, 10, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
            18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
            35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,
            52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68,
            69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85,
            86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100], 
            "outputs/test_write_matrix/bigref.bin")

    def test_16(self):
        self.do_write_matrix("outputs/test_write_matrix/16.bin", 
            1, 6, [23, 45, 56, 67, 78, 89], "outputs/test_write_matrix/16ref.bin")

    def test_61(self):
        self.do_write_matrix("outputs/test_write_matrix/61.bin", 
            6, 1, [23, 45, 56, 67, 78, 89], "outputs/test_write_matrix/61ref.bin")

    def test_empty(self):
        self.do_write_matrix("outputs/test_write_matrix/empty.bin", 
            0, 0, [], "outputs/test_write_matrix/emptyref.bin", 
            fail="fwrite", code=113)

    def test_none(self):
        self.do_write_matrix("outputs/test_write_matrix/none.bin", 
            0, 0, [1, 2, 3], "", 
            fail="fopen", code=112)

    @classmethod
    def tearDownClass(cls):
        print_coverage("write_matrix.s", verbose=False)


class TestClassify(TestCase):

    def make_test(self):
        t = AssemblyTest(self, "classify.s")
        t.include("argmax.s")
        t.include("dot.s")
        t.include("matmul.s")
        t.include("read_matrix.s")
        t.include("relu.s")
        t.include("write_matrix.s")
        return t

    def test_simple0_input0(self):
        t = self.make_test()
        out_file = "outputs/test_basic_main/simple00.bin"
        ref_file = "outputs/test_basic_main/simple00ref.bin"
        args = ["inputs/simple0/bin/m0.bin", "inputs/simple0/bin/m1.bin",
                "inputs/simple0/bin/inputs/input0.bin", out_file]
        #t.input_scalar("a0", 5)
        #t.input_array("a1", t.array(args))
        t.input_scalar("a2", 0)
        # call classify function
        t.call("classify")
        # generate assembly and pass program arguments directly to venus
        t.execute(args=args)
        # compare the output file
        t.check_file_output(out_file, ref_file)
        # TODO
        # compare the classification output with `check_stdout`
        t.check_stdout("2")

    def test_simple0_input1(self):
        t = self.make_test()
        out_file = "outputs/test_basic_main/simple01.bin"
        ref_file = "outputs/test_basic_main/simple01ref.bin"
        args = ["inputs/simple0/bin/m0.bin", "inputs/simple0/bin/m1.bin",
                "inputs/simple0/bin/inputs/input1.bin", out_file]
        #t.input_scalar("a0", 5)
        #t.input_array("a1", t.array(args))
        t.input_scalar("a2", 0)
        # call classify function
        t.call("classify")
        # generate assembly and pass program arguments directly to venus
        t.execute(args=args)
        # compare the output file
        t.check_file_output(out_file, ref_file)
        # TODO
        # compare the classification output with `check_stdout`
        t.check_stdout("2")
    
    def test_simple0_input2(self):
        t = self.make_test()
        out_file = "outputs/test_basic_main/simple02.bin"
        ref_file = "outputs/test_basic_main/simple02ref.bin"
        args = ["inputs/simple0/bin/m0.bin", "inputs/simple0/bin/m1.bin",
                "inputs/simple0/bin/inputs/input2.bin", out_file]
        #t.input_scalar("a0", 5)
        #t.input_array("a1", t.array(args))
        t.input_scalar("a2", 0)
        # call classify function
        t.call("classify")
        # generate assembly and pass program arguments directly to venus
        t.execute(args=args)
        # compare the output file
        t.check_file_output(out_file, ref_file)
        # TODO
        # compare the classification output with `check_stdout`
        t.check_stdout("2")

    def test_simple1_input0(self):
        t = self.make_test()
        out_file = "outputs/test_basic_main/simple10.bin"
        ref_file = "outputs/test_basic_main/simple10ref.bin"
        args = ["inputs/simple1/bin/m0.bin", "inputs/simple1/bin/m1.bin",
                "inputs/simple1/bin/inputs/input0.bin", out_file]
        #t.input_scalar("a0", 5)
        #t.input_array("a1", t.array(args))
        t.input_scalar("a2", 0)
        # call classify function
        t.call("classify")
        # generate assembly and pass program arguments directly to venus
        t.execute(args=args)
        # compare the output file
        t.check_file_output(out_file, ref_file)
        # TODO
        # compare the classification output with `check_stdout`
        t.check_stdout("1")

    def test_simple1_input1(self):
        t = self.make_test()
        out_file = "outputs/test_basic_main/simple11.bin"
        ref_file = "outputs/test_basic_main/simple11ref.bin"
        args = ["inputs/simple1/bin/m0.bin", "inputs/simple1/bin/m1.bin",
                "inputs/simple1/bin/inputs/input1.bin", out_file]
        #t.input_scalar("a0", 5)
        #t.input_array("a1", t.array(args))
        t.input_scalar("a2", 0)
        # call classify function
        t.call("classify")
        # generate assembly and pass program arguments directly to venus
        t.execute(args=args)
        # compare the output file
        t.check_file_output(out_file, ref_file)
        # TODO
        # compare the classification output with `check_stdout`
        t.check_stdout("4")

    def test_simple1_input2(self):
        t = self.make_test()
        out_file = "outputs/test_basic_main/simple12.bin"
        ref_file = "outputs/test_basic_main/simple12ref.bin"
        args = ["inputs/simple1/bin/m0.bin", "inputs/simple1/bin/m1.bin",
                "inputs/simple1/bin/inputs/input2.bin", out_file]
        #t.input_scalar("a0", 5)
        #t.input_array("a1", t.array(args))
        t.input_scalar("a2", 0)
        # call classify function
        t.call("classify")
        # generate assembly and pass program arguments directly to venus
        t.execute(args=args)
        # compare the output file
        t.check_file_output(out_file, ref_file)
        # TODO
        # compare the classification output with `check_stdout`
        t.check_stdout("1")

    def test_simple2_input0(self):
        t = self.make_test()
        out_file = "outputs/test_basic_main/simple20.bin"
        ref_file = "outputs/test_basic_main/simple20ref.bin"
        args = ["inputs/simple2/bin/m0.bin", "inputs/simple2/bin/m1.bin",
                "inputs/simple2/bin/inputs/input0.bin", out_file]
        #t.input_scalar("a0", 5)
        #t.input_array("a1", t.array(args))
        t.input_scalar("a2", 0)
        # call classify function
        t.call("classify")
        # generate assembly and pass program arguments directly to venus
        t.execute(args=args)
        # compare the output file
        t.check_file_output(out_file, ref_file)
        # TODO
        # compare the classification output with `check_stdout`
        t.check_stdout("7")

    def test_simple2_input1(self):
        t = self.make_test()
        out_file = "outputs/test_basic_main/simple21.bin"
        ref_file = "outputs/test_basic_main/simple21ref.bin"
        args = ["inputs/simple2/bin/m0.bin", "inputs/simple2/bin/m1.bin",
                "inputs/simple2/bin/inputs/input1.bin", out_file]
        #t.input_scalar("a0", 5)
        #t.input_array("a1", t.array(args))
        t.input_scalar("a2", 0)
        # call classify function
        t.call("classify")
        # generate assembly and pass program arguments directly to venus
        t.execute(args=args)
        # compare the output file
        t.check_file_output(out_file, ref_file)
        # TODO
        # compare the classification output with `check_stdout`
        t.check_stdout("4")

    def test_simple2_input2(self):
        t = self.make_test()
        out_file = "outputs/test_basic_main/simple22.bin"
        ref_file = "outputs/test_basic_main/simple22ref.bin"
        args = ["inputs/simple2/bin/m0.bin", "inputs/simple2/bin/m1.bin",
                "inputs/simple2/bin/inputs/input2.bin", out_file]
        #t.input_scalar("a0", 5)
        #t.input_array("a1", t.array(args))
        t.input_scalar("a2", 0)
        # call classify function
        t.call("classify")
        # generate assembly and pass program arguments directly to venus
        t.execute(args=args)
        # compare the output file
        t.check_file_output(out_file, ref_file)
        # TODO
        # compare the classification output with `check_stdout`
        t.check_stdout("10")

    def test_noprint(self):
        t = self.make_test()
        out_file = "outputs/test_basic_main/simple22.bin"
        ref_file = "outputs/test_basic_main/simple22ref.bin"
        args = ["inputs/simple2/bin/m0.bin", "inputs/simple2/bin/m1.bin",
                "inputs/simple2/bin/inputs/input2.bin", out_file]
        #t.input_scalar("a0", 5)
        #t.input_array("a1", t.array(args))
        t.input_scalar("a2", 1)
        # call classify function
        t.call("classify")
        # generate assembly and pass program arguments directly to venus
        t.execute(args=args)
        # compare the output file
        t.check_file_output(out_file, ref_file)
        # TODO
        # compare the classification output with `check_stdout`
        t.check_stdout("")

    def test_malloc(self):
        t = self.make_test()
        out_file = "outputs/test_basic_main/student0.bin"
        ref_file = "outputs/test_basic_main/reference0.bin"
        args = ["inputs/simple0/bin/m0.bin", "inputs/simple0/bin/m1.bin",
                "inputs/simple0/bin/inputs/input0.bin", out_file]
        #t.input_scalar("a0", 5)
        #t.input_array("a1", t.array(args))
        t.input_scalar("a2", 0)
        # call classify function
        t.call("classify")
        # generate assembly and pass program arguments directly to venus
        t.execute(args=args, fail="malloc", code=122)

    def test_incorrecta0(self):
        t = self.make_test()
        out_file = "outputs/test_basic_main/student0.bin"
        ref_file = "outputs/test_basic_main/reference0.bin"
        args = ["inputs/simple0/bin/m0.bin", "inputs/simple0/bin/m1.bin",
                "inputs/simple0/bin/inputs/input0.bin", out_file]
        t.input_scalar("a0", 1)
        #t.input_array("a1", t.array(args))
        t.input_scalar("a2", 0)
        # call classify function
        t.call("classify")
        # generate assembly and pass program arguments directly to venus
        t.execute(args=args, code=121)
    

    @classmethod
    def tearDownClass(cls):
        print_coverage("classify.s", verbose=False)


# The following are some simple sanity checks:
import subprocess, pathlib, os
script_dir = pathlib.Path(os.path.dirname(__file__)).resolve()

def compare_files(test, actual, expected):
    assert os.path.isfile(expected), f"Reference file {expected} does not exist!"
    test.assertTrue(os.path.isfile(actual), f"It seems like the program never created the output file {actual}!")
    # open and compare the files
    with open(actual, 'rb') as a:
        actual_bin = a.read()
    with open(expected, 'rb') as e:
        expected_bin = e.read()
    test.assertEqual(actual_bin, expected_bin, f"Bytes of {actual} and {expected} did not match!")

class TestMain(TestCase):
    """ This sanity check executes src/main.S using venus and verifies the stdout and the file that is generated.
    """

    def run_main(self, inputs, input_id, output_id, output_folder, label):
        args = [f"{inputs}/m0.bin", f"{inputs}/m1.bin",
                f"{inputs}/inputs/{input_id}.bin",
                f"outputs/test_{output_folder}_main/{output_id}.bin"]
        reference = f"outputs/test_{output_folder}_main/{output_id}ref.bin"

        t= AssemblyTest(self, "main.s", no_utils=True)
        t.call("main")
        t.execute(args=args)
        t.check_stdout(label)
        if (output_folder != "mnist"):
            t.check_file_output(args[-1], reference)

        #                input folder        input #   outputname  folder  label
    
    def test00(self):
        self.run_main("inputs/simple0/bin", "input0", "simple00", "basic", "2")

    def test01(self):
        self.run_main("inputs/simple0/bin", "input1", "simple01", "basic", "2")

    def test02(self):
        self.run_main("inputs/simple0/bin", "input2", "simple02", "basic", "2")

    def test10(self):
        self.run_main("inputs/simple1/bin", "input0", "simple10", "basic", "1")

    def test11(self):
        self.run_main("inputs/simple1/bin", "input1", "simple11", "basic", "4")

    def test12(self):
        self.run_main("inputs/simple1/bin", "input2", "simple12", "basic", "1")

    def test20(self):
        self.run_main("inputs/simple2/bin", "input0", "simple20", "basic", "7")

    def test21(self):
        self.run_main("inputs/simple2/bin", "input1", "simple21", "basic", "4")

    def test22(self):
        self.run_main("inputs/simple2/bin", "input2", "simple22", "basic", "10")

    def test_mnist0(self):
        self.run_main("inputs/mnist/bin", "mnist_input0", "mnist0", "mnist", "6")

    def test_mnist1(self):
        self.run_main("inputs/mnist/bin", "mnist_input1", "mnist1", "mnist", "9")
    
    # Label = 7
    def test_mnist2(self):
        self.run_main("inputs/mnist/bin", "mnist_input2", "mnist2", "mnist", "9")

    def test_mnist3(self):
        self.run_main("inputs/mnist/bin", "mnist_input3", "mnist3", "mnist", "2")

    def test_mnist4(self):
        self.run_main("inputs/mnist/bin", "mnist_input4", "mnist4", "mnist", "9")

    def test_mnist5(self):
        self.run_main("inputs/mnist/bin", "mnist_input5", "mnist5", "mnist", "4")

    def test_mnist6(self):
        self.run_main("inputs/mnist/bin", "mnist_input6", "mnist6", "mnist", "4")

    # Label = 2
    def test_mnist7(self):
        self.run_main("inputs/mnist/bin", "mnist_input7", "mnist7", "mnist", "8")

    def test_mnist8(self):
        self.run_main("inputs/mnist/bin", "mnist_input8", "mnist8", "mnist", "7")

    

