from sys import stdout

from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics


class FlowStatistics(BestAverageWorstStatistics):
    def write_statistics(self, sender, data_dict):
        print(f'generation #{data_dict["generation_num"]}', file=self.output_stream)
        for index, sub_pop in enumerate(data_dict["population"].sub_populations):
            print(f'subpopulation #{index}', file=self.output_stream)
            best_individual = sub_pop.get_best_individual()
            print(self.format_string.format(best_individual.get_pure_fitness(),
                                            sub_pop.get_worst_individual().get_pure_fitness(),
                                            sub_pop.get_average_fitness()), file=self.output_stream)
            # best_individual.show()

