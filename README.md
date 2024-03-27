# Flow Free Solver
Shahar Bar and Noa Wolfgor

## Flow Free Game
Flow Free is a simple puzzle game.

Each puzzle is a grid contains 2 dots of each color. There are puzzles in a variety of sizes.

<p float="center" align="center">
  <img align="center" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/c8ef63da-df6e-4b32-b1f7-4325027b9fc1" width="252" />
   &emsp;  &emsp;          
  <img align="center" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/b2331871-489e-449e-9f9b-9e9e619725a3" width="397" /> 
</p>

The goal is connecting matching colors with a pipe to create a Flow. 

To solve the puzzle, one needs to pair all colors, and cover the entire board, without pipes cross or overlap.

<p float="center" align="center">
  <img align="center" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/c7950081-fe0a-4a5b-8eb7-44c9099d862d" width="250" />
  &emsp;  &emsp;
  <img align="center" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/f14e538f-6224-4f36-93c3-92c0e0959237" width="401" /> 
</p>

In our project we built a solver to Flow Free puzzles. We used genetic algorithm and some more AI ideas.

## Framing the Problem

Our goal is to solve the Flow Free puzzle.

A simple AI-perspective way to frame the Flow Free puzzle is as a **Constraint Satisfaction Problem** (CSP).

The variables are the free cells in the grid (i.e. cells which do not contain a color dot). The domain of each variable is the all colors (can add a "blank" value for no color). The constraints are:
1. Each cell must be filled by exactly one color (not "blank").
2. Each dot cell must have exactly one adjacent cell in the same color.
3. Each cell which is not a dot cell must have exactly two adjacent cells in the same color.

We combined this idea with genetic algorithm in order to solve the problem.

## Genetic Algorithm (GA)

The genetic algorithm is a method for solving both constrained and unconstrained optimization problems that is based on natural selection, the process that drives biological evolution.

The base idea of natural selection is that "The strong survives". So, taking this idea to the programming world, if we take a (random) population of possible solutions, run on them a program which mimics the process of evolution and repeat it multiple times (generations), we will probably get the best (strongest), or good enough, solution.

The process of evolution includes
- **selection** (those who have survived from the previous generation),
- **crossover** (a child gets genes from both parents),
- **mutation** (sometimes with low probability a gene is changed).

In GA we need to define each of those operators, as well as
- **initial population** (usually random), 
- **fitness evaluator** (evaluate for each individual how much it is good = what is its fitness). 

## Basic Solver 

We used genetic algorithm based on the CSP described above:

<ins>Representing of an individual (solution)</ins>: each cell of the grid (variable) contains exactly one color (value). 

- <ins>initial population</ins> - each individual is a grid where each cell (which is not a dot cell) contains one random color. (dot cells remain as is in every individual and every generation).
- <ins>selection</ins> - tournament selection - the best is chosen from a small group of individuals.
- <ins>crossover</ins> - k-points crossover, i.e. swaps some (randomly chosen) cells among a pair of parents.
- <ins>mutation</ins> - n-points mutation, i.e. randomly change the color (value) of some (randomly chosen) n cells.
- <ins>fitness evaluator</ins> - fitness of individual (grid) is defined to be the sum of fitness of each cell. <br>fitness of cell is defined binary: 1 if the cell satisfied the constraints (dot cell -> exactly one adjacent cell in the same color, other cell -> two adjacent cells in the same color), else 0. <br>That is, the maximum and best fitness is the size (number of cells) of the puzzle.

We found out that this solver works well for small puzzles, but doesn't do well with bigger ones, even if we use a large population and many generations:

<p float="center" align="center">
<img align="center" width="353" alt="Screenshot 2024-03-06 at 21 30 08" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/98264ab6-1440-473f-ae0c-e96383b62ef6"><br>
</p>

An issue we ran into with this representation can be seen in the above.<br>
The fitness of that solution is 43, which is a good fitness compared to the best, 49. however, in actuality it is a very bad solution because the orange path in the bottom left corner has no connection to the dot cells and obviously is not a good path.

This happens since the fitness evaluator gives more points for long paths, even for (obviously) bad paths.

## Re-Framing the Problem

In order to avoid the problem described above, we chose a different representation of the problem.

Our new framing is more similar to the way a human would try to solve a Flow Free puzzle: we want to create paths between each pair of matching colors dot cells, while the goal is
1. no cross or overlap between paths.
2. no cells of the grid which remain empty (i.e. cover the entire board).

With our new framing of the problem we built a better genetic-algorithm based solver.

## Paths Based Solver

We used genetic algorithm based on the representation of the problem described above:

<ins>Representing of an individual (solution)</ins>: each color has a single path between the two dot cells (if succeed to generate it, else has no path).

- <ins>initial population</ins> - each individual is a grid that contains a randomly generated path between the two dot cells for each color (or no path if not succeed to generate one).
- <ins>selection</ins> - tournament selection - the best is chosen from a small group of individuals.
- <ins>crossover</ins> - colors crossover, i.e. swaps paths of some (randomly chosen) colors among a pair of parents.
- <ins>mutation</ins> - n-colors mutation, i.e. change the path (randomly generate the new path) of some n (randomly chosen) colors.
- <ins>fitness evaluator</ins> - fitness of individual (grid) is defined to be the number of collisions among paths (per cell). Each color with no path increase the fitness by number of colors squared. Notice that now we want to minimize the fitness, and the minimum and best fitness is 0.

## Optimizations

The paths based solver did better, but it still needed too large population and too many generations to converge a solution, espicially in big puzzles.

We have implemented further optimizations.

### Legal Paths and DeadEnd Checks

We optimized the random path generation function in two aspects:

1. **Legal Paths Only** - We modified the generate path function to generate only legal paths and avoid illegal paths which will be noise and keeps GA away from finding the solution.<br> A path is legal if
   - It doesnt go through a dot cell. 
   - It doesnt contain unnecessary parts, such as<br><br> 
     <img width="249" alt="Screenshot 2024-03-06 at 22 49 36" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/b77112b5-9acf-4df3-9998-2e3343beeab6"><br>
   

2. **DeadEnd Checks** - We modified the generate path function to reject DeadEnd paths, which will be noise and keeps GA away from finding the solution.
   <br>A DeadEnd path is a path that will not be consistent with any complete solution. There are some kinds of DeadEnd path:
    - **Block a color.** i.e. there is no path between the both dots of a color without cross the DeadEnd path. <br><br>
      <img width="351" alt="Screenshot 2024-03-06 at 23 03 48" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/d111269d-aad3-4fbc-87fd-d35a36fa7536"><br>
      The blue color is blocked.
    - **Block cells.** i.e. there are cells which cannot be filled without cross the DeadEnd path.
      <p float="left" align="left">
      <img align="center" width="351" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/1996eafb-9b0c-4348-acc0-e204b550dcc9" />
      &emsp;  &emsp;
      <img align="center" width="351" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/6eeea958-618c-4276-910c-5b9394eb135f" /> 
      </p>
      The bottom left corner cells are blocked. &emsp;  &emsp; &emsp;  &emsp; &emsp;  
      The single cell surrounded by the blue path is blocked.

### Smart Crossover and Smart Mutation

Since generate path can fail, there are individuals which has no path of some colors. We implemented a smart version of crossover and mutation operator:
- **Smart Crossover** - For each color, if only one of the parents has a path of that color, it is determined that this color will be taken from that parent. else it is chosen randomly one of the parents.
- **Smart Mutation** -
  - version 1: mutation with high probability to generate path for color which the individual has no path of.
  - version 2: mutation that chooses color smartly by choosing a color which his path colliding with another path (randomly chosen from all such colors). 

## Arc Consistency

After all optimizations above, the solver worked very good on medium puzzles but still needed too large population and too many generations for the big puzzles (with size >= 10).

Our idea was to reduce the problem space, so the solver will succeed also with the bigger puzzles.

For that purpose we used Arc Consistency algorithm, which works on CSP. 

We returned to our first framing of the problem as CSP, and run the Arc Consistency algorithm first. The idea of 
the algorithm is to eliminates values from domain of variable that can never be part of a consistent solution. 

Our implementation for Flow Free puzzle actually determine color of cells which must be filled with that color.<br> For example, <br>
<img align="center" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/c8ef63da-df6e-4b32-b1f7-4325027b9fc1" width="252" > <br>
The bottom right corner cell must be orange. <br>
<img width="253" alt="Screenshot 2024-03-07 at 1 03 52" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/b8b07afa-83a2-4aa1-bfc7-22b4d6a3ba5e"> <br>
Next, the cell above must be orange as well. And so on...<br>

The result is a smaller problem space, where the colors of cells that the algorithm determined are fixed. 

We found out that for small puzzles, Arc Consistency itself solves the puzzles:
<p float="center" align="center">
<img align="center" width="300" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/703a5406-a0dc-4cf2-bde2-e4a01ded1cee" />
&emsp;  &emsp;
<img align="center" width="353" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/ed6e7c08-4b2f-4b51-b569-e90891209164" /> 
</p>

And for lots of the big puzzles it achieves really good results:
<p float="center" align="center">
<img align="center" width="451" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/31a51169-6187-4553-bc31-5faeaa436074" />
&emsp; 
<img align="center" width="500" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/17d95b3e-8e0e-42a4-b9bf-b8323695c758" /> 
</p>

## Our Flow Free Solver

- Initially, run Arc Consistency to get more constrained space of the problem and define a constrained version of the problem, with fixed cells (which determined in Arc Consistency). <br>After this step problem space is reduced.
- Then run Paths Based Solver on the constrained version of the problem, including optimizations in path generation and smart crossover+mutation as mentioned above.
- Finally get great solutions!

<p float="center" align="center">
<img align="center" width="501" alt="Screenshot 2024-03-07 at 1 28 56" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/6a06ee21-d123-468a-adb8-9f2c3d35e9db">
</p>

## Code Overview

We use EC-KitY - Python tool kit for doing evolutionary computation. 

We use tkinter - Python package for the GUI parts. 

We use matplotlib - Python library for the statistics part.

- paths_based_solver
  - arc_consistency
    - **ArcConsistency.py** class ArcConsistency contains the arc consistency implementation.
      - function **arc_consistency** implement the Arc Consistency algorithm
      - function **convert_to_smaller_problem** define a constrained version of the problem
  - boards
    - **Board.py** class Board contain all data needed for board representation.
    - **ArcConsistencyBoard.py** class ArcConsistencyBoard support board representation with fixed cells.
  - GA
    - **BoardIndividual.py** class BoardIndividual extends class Individual of eckity. Individual represents a board.
    - **FlowCreator.py** class FlowCreator extends class Creator of eckity. Create individuals by generating path for each color on board.
      - function **generate_path** implement the random generating path.
      - function **detect_deadend_path** detect DeadEnd path in order to reject them.
    - **FlowCrossover.py** class FlowCrossover extends class GeneticOperator of eckity. Implement the crossover operator.
      - function **random_partition** implement the default crossover by random partition of colors to crossover.
      - function **smart_partition** implement the optimization of smart crossover by choosing the partition smartly.
    - **FlowEvaluator.py** class FlowEvaluator extends class SimpleIndividualEvaluator of eckity. Compute the fitness value by counting collisions.
    - **FlowNColorsMutation.py** class FlowNColorsMutation extends class FailableOperator of eckity. Implement the mutation operator.
      - function **default_color_selector** implement the default mutation by randomly choosing color for mutation.
      - function **good_color_selector** implement the optimization of smart mutation with high prbability to generate path for color which the individual has no path of.
      - function **smart_color_selector** implement the optimization of smart mutation that chooses color smartly by choosing a color which his path colliding with another path.
    - **FlowTerminationChecker.py** class FlowTerminationChecker extends class TerminationChecker of eckity. The termination condition is best fitness = 0.
    - **FlowStatistics.py** class FlowStatistics extends class BestAverageWorstStatistics of eckity. Storing the Fitness statistics for each generation.
    - **FlowGA.py** class FlowGA storing all the data needed for running the genetic algorithm with eckity.
      - function **run** run genetic algorithm with eckity.
      - function **get_solved_matrix** convert the board of the best individual to a solved board that can be printed.
  - gui
    - **Color.py** Enum of colors.
    - **FlowGUI.py** implement of GUI for board.
  - statistics
    - **plot.py** plot the statistics of GA runs.
  - **main.py** the main program. Let the user choose a puzzle and try to solve it.
    - function **main** using default population size and number of generations according to the chosen board's size, support increasing them if the run did not converge.
    - function **run_for_statistics** run 3 times the GA on the chosen board and plot the results. The population size and number of generations are to the user's choice.
  - **Puzzles.py** contain a variety of Flow Free puzzles.

## Extention for Hard Puzzles

We tried to run our solver on hard puzzles (size > 10).

<p float="center" align="center">
<img width="547" alt="Screenshot 2024-03-07 at 2 30 14" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/6aa9c998-fa7e-4f27-8964-43563f219fb7">
</p>

Results:

With population=1000 and generations=50 we get:<br>
Fitness: 22<br>
<img width="551" alt="Screenshot 2024-03-07 at 2 31 48" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/20d8c8f0-b73d-4c3e-ae12-cfb4b6db23bf">

With population=2000 and generations=75 we get:<br>
Fitness: 8<br>
<img width="550" alt="Screenshot 2024-03-07 at 2 32 58" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/3aba2a09-111b-4ea6-90d1-1350d41a3700">

With population=4000 and generations=125 (after 3 runs) we get:<br>
Fitness: 2<br>
<img width="552" alt="Screenshot 2024-03-07 at 10 59 42" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/effaaa3d-f232-40c6-87a6-1867aac7c9d5">

## Statistics and Takeaways

We examine the best fitness achieved by using different population sizes, with different sizes of puzzles. 

Since it is a random algorithm, one run is not representative. So, we examine the results for 3 or more runs. 

Since the fitness is much higher in the beginning, the plot starting from generation #5, so we can see the fluctuations in the graph better.

### Results:

<ins>Puzzles of size <= 8:</ins> converge to solution (fitness 0) in only few generations (even less than 10) using population of 300+. But using smaller population, it takes much more generations and even sometimes does not converge. <br>Notice that there exists puzzles that completely solved by Arc Consistency itself. 

<ins>Puzzles of size 9x9:</ins>

![Screenshot 2024-03-27 at 23 06 04](https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/05070533-7359-4c8c-aa89-0afb40e42541)

![Screenshot 2024-03-27 at 23 08 21](https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/ed3facd8-60be-44c3-8dda-1784df489e87)

<ins>Puzzles of size 10x10:</ins>

![Screenshot 2024-03-27 at 23 57 40](https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/480b45a9-a503-4561-9c4e-341357c78b12)

![Screenshot 2024-03-28 at 0 15 12](https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/12314f84-d2e8-49c6-8c0a-8b1391cc7ddf)

![Screenshot 2024-03-28 at 0 23 16](https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/e710e322-a11c-46cf-bb21-61b5addcf1e3)

<ins>Puzzles of size > 10:</ins> Usually did not converge with many generations and large population, but one can see an improvment in the best fitness as
 the population size grows. For example: puzzle size 12x12: with population 1000: after 1000 generations it achieved fitness 24. with population 2000: after 1000 generations it achieved fitness 20. 

### Conclusions

- Population size has the greatest effect on convergence! With big enough population the convergence is relatively fast, while with a small population it usually does not converge to solution, even with much many generations.<br> This phenomenon occurs because the convergence of the algorithm is highly dependent on the initial random population, from which the individuals keep getting better and better and converge to a better solution. If the population is small, there are much less random paths that generated in the initial step. As a result, we miss a lot of possible paths. In this situation, even the convergence of all individuals to a best individual will not achieve a complete solution. <br>(Note that although the mutation operator generates new paths as well, it happens on a much smaller scale than in the initial step).

- Number of population that required for convergence depends on the board size. While small and medium puzzles (size < 9) works well with population of 300-500, the big puzzles (size between 9-10) requires 1000-2000, and even more is required for the hard (huge) puzzles (size > 10). <br> This is happen since the number of possible paths grows exponentially in board size.

- In practice: The population size is defined to be 500 for puzzles of size < 10 and 1000 for size >= 10. There is an option to enlarge that and try again if the algorithm did not converge to a solution. The number of generations is defined to be 200 for puzzles of size < 10 and 500 for size >= 10, and it grows with the population size.

- Arc Consistency works very well of some puzzles! For example, it can reduce the problem space of a puzzle of size 9 or 10 to be as a puzzle of size 6 or 7. As a result, we need much less population and generations for those puzzles even though they are big puzzles, and the run takes much less time. This is a big improvement!

## How to Run

- Install python packages: tkinter, eckity, matplotlib. You can use pip install.
- Run paths_based_solver/main.py
