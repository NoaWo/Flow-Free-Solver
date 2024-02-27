import random

from eckity.genetic_operators.genetic_operator import GeneticOperator


class FlowCrossover(GeneticOperator):
    def __init__(self, rows, columns, colors, random_partition_size=False, probability=1, arity=2, events=None):
        self.individuals = None
        self.applied_individuals = None
        self.colors = colors
        self.rows = rows
        self.columns = columns
        self.partition1 = None
        self.partition2 = None
        self.random_partition_size = random_partition_size
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
        self.partition1, self.partition2 = self.random_partition()

        i1 = individuals[0]
        i2 = individuals[1]

        # crossover paths
        for i in range(self.rows):
            for j in range(self.columns):
                cell1 = i1.get_cell(i, j)
                cell2 = i2.get_cell(i, j)
                new_cell1, new_cell2 = self.crossover_cell(cell1, cell2)
                i1.set_cell(i, j, new_cell1)
                i2.set_cell(i, j, new_cell2)

        # crossover has_path
        self.crossover_has_path()

        self.applied_individuals = individuals
        return individuals

    def random_partition(self):
        colors = [i for i in range(1, self.colors + 1)]
        random.shuffle(colors)

        partition_size = len(colors) // 2
        if self.random_partition_size:  # todo
            partition_size = random.randint(1, self.colors - 1)

        partition_1 = colors[:partition_size]
        partition_2 = colors[partition_size:]

        return partition_1, partition_2

    def crossover_cell(self, colors_cell1, colors_cell2):
        remain_colors_cell1 = [color for color in colors_cell1 if color < 0 or color in self.partition1]
        remain_colors_cell2 = [color for color in colors_cell2 if color < 0 or color in self.partition2]
        new_colors_cell1 = remain_colors_cell1 + [color for color in remain_colors_cell2 if color > 0]
        new_colors_cell2 = remain_colors_cell2 + [color for color in remain_colors_cell1 if color > 0]
        return new_colors_cell1, new_colors_cell2

    def crossover_has_path(self):
        i1 = self.individuals[0]
        i2 = self.individuals[1]
        for color in self.partition1:
            i2.set_has_path_of(color, i1.has_path_of(color))
        for color in self.partition2:
            i1.set_has_path_of(color, i2.has_path_of(color))