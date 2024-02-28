import random

from eckity.genetic_operators.failable_operator import FailableOperator

from BoardIndividual import BoardIndividual


class FlowNColorsMutation(FailableOperator):
    def __init__(self,
                 colors,
                 rows,
                 columns,
                 generate_path,
                 # deadend_paths,
                 n=1,
                 probability=1.0,
                 arity=1,
                 is_smart=False,
                 color_selector=None,
                 events=None,
                 attempts=3):
        super().__init__(probability=probability, arity=arity, events=events, attempts=attempts)
        self.n = n
        self.colors = colors
        self.rows = rows
        self.columns = columns
        self.generate_path = generate_path

        if color_selector is None:
            color_selector = self.default_color_selector
        if is_smart:
            color_selector = self.smart_color_selector
        self.color_selector = color_selector
        # self.deadend_paths = deadend_paths
        self.color_attempts = attempts

    def default_color_selector(self, ind):
        return random.sample(range(1, self.colors + 1), k=self.n)

    def smart_color_selector(self, ind):
        colors_to_mutate = self.find_collision(ind)
        # colors_to_mutate = [color for color in range(1, self.colors + 2) if not ind.has_path_of(color) or ind.is_bad_path_of(color)]
        k = self.n
        if len(colors_to_mutate) < k:
            k = len(colors_to_mutate)
        return random.sample(colors_to_mutate, k=k)

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
            colors_mutation = self.color_selector(individual)

            for color in colors_mutation:
                for _ in range(self.color_attempts):
                    dots = individual.get_dots_of(color)
                    new_path = self.generate_path(dots[0], dots[1])
                    # todo add a check if it is deadend path
                    if new_path is None: # or (color, tuple(new_path)) in self.deadend_paths:
                        succeeded = False
                        # continue
                    else:
                        self.replace_path(new_path, color, individual)
                        succeeded = True
                        break

        self.applied_individuals = individuals
        return True, individuals
        # return succeeded, individuals

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
        individual.set_has_path_of(color, True)
        individual.set_bad_path_of(color, False)

    def find_collision(self, individual):
        collisions = [False for _ in range(self.colors + 1)]
        for i in range(self.rows):
            for j in range(self.columns):
                colors_cell = individual.get_cell(i, j)
                if len(colors_cell) > 1:
                    for color in colors_cell:
                        if color < 0:
                            raise ValueError("Collision in dot cell")
                        collisions[color] = True
        colors_that_collide = [color for color in range(1, self.colors + 1) if collisions[color]]
        return colors_that_collide
