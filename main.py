import random

from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        number_of_columns = self.read_input()
        matrix = [[0 for _ in range(number_of_columns)] for _ in range(number_of_columns)]
        vec = [0 for _ in range(number_of_columns)]

        for i in range(0, number_of_columns):
            vec[i] = random.uniform(0, 10)
            for j in range(0, number_of_columns):
                matrix[i][j] = random.uniform(0, 10)

        # map

        number_of_workers = len(self.workers)
        step = int(number_of_columns / number_of_workers)
        mapped = []
        for i in range(0, number_of_workers):
            if i == number_of_workers - 1:
                last_index = number_of_columns
            else:
                last_index = i * step + step
            mapped.append(self.workers[i].mymap(matrix, vec, i * step, last_index))

        print
        'Map finished: ', mapped

        # reduce
        reduced = self.myreduce(mapped)
        print("Reduce finished: " + str(reduced))

        # output
        self.write_output(reduced, matrix, vec)

        print("Job Finished")

    @staticmethod
    @expose
    def mymap(matrix, vec, a, b):
        number_of_columns = len(matrix)
        result = []
        for i in range(a, b):
            res = ""
            sum = 0
            for k in range(0, number_of_columns):
                sum += matrix[i][k] * vec[k]
            res += '%.2f' % sum + " "
            result.append(res)
        print(result)
        return result

    @staticmethod
    @expose
    def myreduce(mapped):
        res = []
        for x in mapped:
            res.extend(x.value)
        return res

    def read_input(self):
        f = open(self.input_file_name, 'r')
        number_of_column = int(f.readline())
        f.close()
        return number_of_column

    def write_output(self, output, matrix, vec):
        f = open(self.output_file_name, 'w')
        number_of_columns = len(matrix)
        for i in range(0, number_of_columns):
            for j in range(0, number_of_columns):
                f.write('%.2f' % matrix[i][j] + " ")
            f.write("\n")
        f.write("\n \n")
        for i in range(0, number_of_columns):
            f.write('%.2f' % vec[i] + " ")
        f.write("\n \n")
        for x in output:
            f.write(str(x))
        f.close()
        print(output)


# if __name__ == '__main__':
#     master = Solver([Solver(), Solver(), Solver()],
#                     "C:/Users/gladk/Desktop/input.txt",
#                     "C:/Users/gladk/Desktop/output.txt")
#     master.solve()
