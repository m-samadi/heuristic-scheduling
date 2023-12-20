# Heuristic task-to-thread scheduling
This simulator performs task-to-thread scheduling for OpenMP-based programs using the heuristic method and some of the existing methods.
<br/>
<br/>
## Specification
The graphs can be generated in the simulator based on the benchmark or randomly. The task execution time is calculated using the minimum, average, or maximum function. The application deadline is determined based on the volume of graph and a random number. For each method, the response time, status of the missed deadline, idle times of threads, and static scheduling of tasks in threads are determined at the end of the simulation process. Moreover, graphical results can be also generated to illustrate the scheduling steps of tasks. After scheduling the graph using each algorithm, the response times, idle times, and missed deadlines obtained from all the methods are exported to a file.
<br/>
<br/>
As this simulator is used to schedule the graphs used in the provided benchmarks and the task execution times are high numbers, the time interval for the loop in the code of each method is set to 1000000 (i.e., t += 1000000) by default. But you can set it to 1 to simulate random graphics or other benchmarks.
<br/>
<br/>
## Simulation parameters
The simulation parameters are set by default. But they can be changed at the beginning of main.py before the simulation process based on the requirements of the application applied.
<br/>
<br/>
## Graphical output
Graphical outputs can be generated at the end of the simulation process by considering the variable 'graphic_result' as 1. Note that there is a limitation in drawing the shapes in Python. Therefore, if number of tasks is high, keep this feature disabled.
<br/>
<br/>
## Benchmark
Five benchmarks are provided in the simulator (placed in the benchmark folder), including a DOT file (which contains the task ID and data dependencies of the tasks) and a JSON file (which contains multiple execution times for each task). However, two of them (i.e., hog and wavefront) do not include the JSON file, as they have not been used in the simulation results. Furthermore, two JSON files are provided for the simulated benchmarks, where the task execution time can be considered based on 4 threads and 8 threads, as the execution time of the tasks is measured under these configurations. To use them in the simulator, simply rename one of the files to bench_json (where bench is the name of the benchmark) before simulation. Note that the execution times are measured using the Extrae [1] and Papi [2] tools, as well as the JSON file is created with a script [3] and the Paraver toolset [4].
<br/>
<br/>
Additionally, any new benchmarks can be easily added to this set and used in the simulator, following the structures of the existing DOT and JSON files.
<br/>
<br/>
## Execution
The simulation process is executed with the following command:
```
python main.py
```
If the DAG needs to be generated based on the benchmark, press 'y'; otherwise press 'n'.
<br/>
<br/>
## References
[1] Barcelona Supercomputing Center (BSC), "Extrae," December 2023. https://tools.bsc.es/extrae/
<br/>
[2] Innovative Computing Laboratory, University of Tennessee, "Performance Application Programming Interface, PAPI," April 2023. https://icl.utk.edu/papi/index.html/
<br/>
[3] Barcelona Supercomputing Center (BSC), "TDG instrumentation," December 2023. https://gitlab.bsc.es/ampere-sw/wp2/tdg-instrumentation-script/
<br/>
[4]	A. Munera, S. Royuela, G. Llort, E. Mercadal, F. Wartel, and E. Quiñones, "Experiences on the characterization of parallel applications in embedded systems with extrae/paraver," in Proc. of the 49th Int. Conference on Parallel Processing (ICPP '20), Edmonton, AB, Canada, pp. 1–11, August 17–20, 2020.
