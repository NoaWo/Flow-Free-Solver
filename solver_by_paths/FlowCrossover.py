import random

from eckity.genetic_operators.genetic_operator import GeneticOperator


class FlowCrossover(GeneticOperator):
    def __init__(self, rows, columns, colors, random_partition_size=False,
                 probability=1, arity=2, events=None, is_smart=False):
        self.individuals = None
        self.applied_individuals = None
        self.colors = colors  # colors = {1,...,self._colors-1}
        self.rows = rows
        self.columns = columns
        self.partition1 = None
        self.partition2 = None
        self.random_partition_size = random_partition_size
        self.is_smart = is_smart
        super().__init__(probability=probability, arity=arity, events=events)

    def apply(self, individuals):
        """
        Attempt to perform the crossover operator

        Parameters
        ----------
        individuals : list of individuals
            individuals to perform crossover on

        Returns
        ----------
        list of individuals
            individuals after the crossover
        """
        self.individuals = individuals
        if not self.is_smart:
            self.partition1, self.partition2 = self.random_partition()
        else:
            self.partition1, self.partition2 = self.smart_partition()

        i1 = individuals[0]
        i2 = individuals[1]

        # crossover paths
        for i in range(self.rows):
            for j in range(self.columns):
                cell1 = i1.get_cell(i, j)
                cell2 = i2.get_cell(i, j)
                new_cell1 = self.crossover_cell(cell1, cell2, self.partition1, self.partition2)
                new_cell2 = self.crossover_cell(cell2, cell1, self.partition1, self.partition2)
                i1.set_cell(i, j, new_cell1)
                i2.set_cell(i, j, new_cell2)

        i1_has_path = i1.get_has_path()
        i2_has_path = i2.get_has_path()
        # crossover has_path
        self.crossover_has_path(i1, self.partition2, i2_has_path)
        self.crossover_has_path(i2, self.partition2, i1_has_path)

        self.applied_individuals = individuals
        return individuals

    def random_partition(self):
        colors = [i for i in range(1, self.colors)]
        random.shuffle(colors)

        partition_size = len(colors) // 2
        if self.random_partition_size:
            partition_size = random.randint(1, self.colors - 2)

        partition_1 = colors[:partition_size]
        partition_2 = colors[partition_size:]

        return partition_1, partition_2

    @staticmethod
    def crossover_cell(colors_cell1, colors_cell2, partition_1, partition_2):
        colors_from_1 = [color for color in colors_cell1 if color in partition_1 or color < 0]
        colors_from_2 = [color for color in colors_cell2 if color in partition_2]
        new_cell = colors_from_1 + colors_from_2
        return new_cell

    @staticmethod
    def crossover_has_path(i1, partition2, i2_has_path):
        for color in partition2:
            i1.set_has_path_of(color, i2_has_path[color])

    def smart_partition(self):
        i1 = self.individuals[0]
        i2 = self.individuals[1]
        partition1 = []
        partition2 = []
        colors = [i for i in range(1, self.colors)]
        for color in colors:
            if i1.has_path_of(color) and i2.has_path_of(color):
                coin = random.randint(1, 2)
                if coin == 1:
                    partition1.append(color)
                if coin == 2:
                    partition2.append(color)
            elif i1.has_path_of(color):
                partition1.append(color)
            elif i2.has_path_of(color):
                partition2.append(color)
            else:
                coin = random.randint(1, 2)
                if coin == 1:
                    partition1.append(color)
                if coin == 2:
                    partition2.append(color)
        return partition1, partition2
