# Flow Free Solver
Written by Shahar Bar and Noa Wolfgor

## Flow Free Game
Flow Free is a simple yet addictive puzzle game.

Each puzzle is a grid contains 2 dots of each color. There are puzzles in a variety of sizes.

<p float="center" align="center">
  <img align="center" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/c8ef63da-df6e-4b32-b1f7-4325027b9fc1" width="252" />
   &emsp;  &emsp;          
  <img align="center" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/b2331871-489e-449e-9f9b-9e9e619725a3" width="397" /> 
</p>

The goal is connecting matching colors with pipe to create a Flow. 

To solve the puzzle, one needs to pair all colors, and cover the entire board, without pipes cross or overlap.

<p float="center" align="center">
  <img align="center" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/c7950081-fe0a-4a5b-8eb7-44c9099d862d" width="250" />
  &emsp;  &emsp;
  <img align="center" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/f14e538f-6224-4f36-93c3-92c0e0959237" width="401" /> 
</p>

## Framing the Problem

A simple AI-perspective way to frame the Flow Free puzzle is as a **Constraint Satisfaction Problem** (CSP).

The variables are the free cells in the grid (i.e. cells which not contain a color dot). The domain of each variable is the all colors (can add a "blank" value for no color). The constraints are:
1. Each cell must be filled by exactly one color.
2. Each dot cell must has exactly one adjacent cell in the same color.
3. Each cell which is not a dot cell must has exactly two adjacent cells in the same color.

We combined this idea with genetic algorithm in order to solve the problem.

## Genetic Algorithm (GA)

The genetic algorithm is a method for solving both constrained and unconstrained optimization problems that is based on natural selection, the process that drives biological evolution.

The base of natural selection is that "The strong survives". So, taking this idea to the programming world, if we take a (random) population of possible solutions, run on them a program which mimics the proccess of evolution and reapet it lots of times (generations), we probably get the best (strongest) solution.

Proccess of evolution includes
- **selection** (who has survived from the last generation),
- **crossover** (a child gets genes from both parents),
- **mutation** (sometimes with low probability a gene is changed).

In GA we need to define each of those operators, as well as
- **initial population** (usually random), 
- **fitness evaluator** (evaluate for each individual how much it is good = what is its fitness). 

## Basic Solver 

We used genetic algorithm based on the CSP described above:

Representing of a solution: each cell (variable) contains exactly one color (value). 

- initial population - each individual is a grid where each cell (which is not a dot cell) contains one random color.
- selection - tournament selection - the best is chosen from a small group of individuals.
- crossover - k-points crossover, i.e. swaps some (randomly chosen) cells among a pair of parents.
- mutation - n-points mutation, i.e. randomly change the color (value) of a n cells (randomly chosen).
- fitness evaluator - fitness of individual (grid) is defined to be the sum of fitness of each cell. fitness of cell is defined binary: 1 if the cell satisfied the constraints (dot cell -> exactly one adjacent cell in the same color, other cell -> two adjacent cells in the same color), else 0. That is, the maximum (and best) fitness is the size (number of cells) of the puzzle.

We found out that this solver solves well small puzzles, but gets troubled with bigger ones, even with a large population and many generations:

<p float="center" align="center">
<img align="center" width="353" alt="Screenshot 2024-03-06 at 21 30 08" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/98264ab6-1440-473f-ae0c-e96383b62ef6"><br>
</p>

For example, the fitness of the individual (solution) above is 43 (which is a good fitness comparing to the best fitness 49), but actually it is a very bad solution since the orange path in the bottom left corner has no connection to the dot cells and obviously is not a good path.

This happens since the fitness evaluator gives more points for long paths, even though for (obviously) bad paths.

## Re-Framing the Problem

In order to avoid the problem described above, we chose a different representing of the problem.

Our new framing is more similar to the way a human try to solve a Flow Free puzzle: we want to create paths between each pair of matching colors dot cells, while the goal is
1. no cross or overlap between paths
2. no cells which remain empty (cover the entire board)

With that framing of the problem we build a better genetic-algorithm based solver.

## Paths Based Solver

We used genetic algorithm based on the representing of the problem described above:

Representing of a solution: each color has a single path between the two dot cells (if succeed to generate it).

- initial population - each individual is a grid contains a randomly generated path between the two dot cells for each color (or no path if not secceed generate one).
- selection - tournament selection - the best is chosen from a small group of individuals.
- crossover - colors crossover, i.e. swaps paths of some colors (randomly chosen) among a pair of parents.
- mutation - n-colors mutation, i.e. change the path (randomly generated) of n colors (randomly chosen).
- fitness evaluator - fitness of individual (grid) is defined to be the number of collisions among paths (per cell). Notice that now we want to minimize the fitness, and the minimum and best fitness is 0.

## Optimizations

That solver worked better, but it still needed too large population and too many generations to converge a solution, espicially in big puzzles.

We have implemented some optimizations.

### Optimization: Legal Paths and DeadEnd Checks

We optimized the randomly generate path function in two aspects:

1. **Legal Paths Only** - We modified the generate path function to generate only legal paths and avoid illegal paths which will be noise and keeps GA away from finding the solution.<br> A path is legal if
   - It doesnt go through a dot cell. 
   - It doesnt contain unnecessary parts, such as<br><br> 
     <img width="249" alt="Screenshot 2024-03-06 at 22 49 36" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/b77112b5-9acf-4df3-9998-2e3343beeab6"><br>
   

2. **DeadEnd Checks** - We modified the generate path function to reject DeadEnd paths, which will be noise and keeps GA away from finding the solution.
   <br>A DeadEnd path is a path that will not be consistent with a complete solution. There are some kinds of DeadEnd path:
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
      The single cell which surrounded by the blue path is blocked.

### Optimization: Smart Crossover and Smart Mutation

Since generate path can fail, there are individuals which has no path of some colors. We implemented smart version of crossover and mutation operator:
- **Smart Crossover** - For each color, if only one of the parents has a path of that color, it determined that this color will be taken from that parent. else it choose randomly one of the parents.
- **Smart Mutation** -
  - version 1: mutation with high prbability to generate path for color which the individual has no path of.
  - version 2: mutation that chooses color smartly by choosing a color which his path colliding with another path (randomly chosen from all such colors). 

## Arc Consistency

After all optimizations above, the solver worked very good on medium puzzles but still needed too large population and too many generations for the big puzzles (with size >= 10).

Our idea was to reduce the problem space, so the solver will succeed also with the bigger puzzles.

For that purpose we used Arc Consistency algorithm, which works on CSP. 

We returned to our first framing of the problem as CSP, and run the Arc Consistency algorithm first. The idea of 
the algorithm is to eliminates values from domain of variable that can never be part of a consistent solution. 

Our implement for Flow Free puzzle actually determine color of cells which must be filled with that color.<br> For example, <br>
<img align="center" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/c8ef63da-df6e-4b32-b1f7-4325027b9fc1" width="252" > <br>
The bottom right corner cell must be orange. <br>
<img width="253" alt="Screenshot 2024-03-07 at 1 03 52" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/b8b07afa-83a2-4aa1-bfc7-22b4d6a3ba5e"> <br>
Next, the cell above must be orange as well. And so on...<br>

The result is a smaller problem space, where the cells that the algorithm determined are fixed. 

We found out that for small puzzles, Arc Consistency itself solves the puzzles:
<p float="center" align="center">
<img align="center" width="300" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/703a5406-a0dc-4cf2-bde2-e4a01ded1cee" />
&emsp;  &emsp;
<img align="center" width="353" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/ed6e7c08-4b2f-4b51-b569-e90891209164" /> 
</p>

And for lots of the big puzzles it achives really good results:
<p float="center" align="center">
<img align="center" width="451" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/31a51169-6187-4553-bc31-5faeaa436074" />
&emsp; 
<img align="center" width="500" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/17d95b3e-8e0e-42a4-b9bf-b8323695c758" /> 
</p>

## Our Flow Free Solver

We run Arc Consistency first, get more constrained space of the problem, i.e. problem space is reduced. Then we define a constrained version of the problem, with fixed cells (which determined in Arc Consistency). On that constrained version of the problem, we run the Paths Based Solver and get great solutions!

<p float="center" align="center">
<img align="center" width="501" alt="Screenshot 2024-03-07 at 1 28 56" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/6a06ee21-d123-468a-adb8-9f2c3d35e9db">
</p>

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

With population=7000 and generations=200 we get (after a long run):<br>
Fitness: 4<br>
<img width="549" alt="Screenshot 2024-03-07 at 2 58 23" src="https://github.com/NoaWo/Flow-Game-Solver/assets/135462814/7c96b5b8-e2b8-48e2-b0f7-121bb3af7801">
