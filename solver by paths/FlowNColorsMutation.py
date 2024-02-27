import random

from eckity.genetic_operators.failable_operator import FailableOperator

from genetic_algorithm.BoardIndividual import BoardIndividual


class FlowNColorsMutation(FailableOperator):
    def __init__(self,
                 colors,
                 rows,
                 columns,
                 generate_path,
                 n=1,
                 probability=1.0,
                 arity=1,
                 color_selector=None,
                 events=None,
                 attempts=5):
        super().__init__(probability=probability, arity=arity, events=events, attempts=attempts)
        self.n = n
        self.colors = colors
        self.rows = rows
        self.columns = columns
        self.generate_path = generate_path

        if color_selector is None:
            color_selector = self.default_color_selector
        self.color_selector = color_selector

    def default_color_selector(self):
        return random.sample(range(1, self.colors + 1), k=self.n)

    def attempt_operator(self, individuals, attempt_num):
        """
        Attempt to perform the mutation operator

        Parameters
        ----------
        individuals : list of BoardIndividual
            BoardIndividual to mutate

        attempt_num : int
            Current attempt number

        Returns
        ----------
        tuple of (bool, list of BoardIndividual)
            first return value determines if the attempt succeeded
            second return value is the operator result
        """
        succeeded = True
        for individual in individuals:
            # old_individual = individual.clone()

            # randomly select n colors (without repetitions)
            colors_mutation = self.color_selector()

            for color in colors_mutation:
                dots = individual.get_dots_of(color)
                new_path = self.generate_path(dots[0], dots[1])
                if new_path is not None:
                    self.replace_path(new_path, color, individual)
                else:
                    succeeded = False

        self.applied_individuals = individuals
        return True, individuals

    def on_fail(self, payload):  # todo
        """
        The required fix when the operator fails, does nothing by default and can be overridden by subclasses

        Parameters
        ----------
        payload : object
            relevant data for on_fail (usually the individuals that the mutation was attempted to be applied on)
        """
        pass

    def replace_path(self, new_path, color, individual):
        for i in range(self.rows):
            for j in range(self.columns):
                curr_cell = (i, j)
                colors_cell = individual.get_cell(i, j)
                if color in colors_cell:
                    colors_cell.remove(color)
                if curr_cell in new_path:
                    colors_cell.append(color)
                individual.set_cell(i, j, colors_cell)

