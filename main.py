 #**************************************************************************
 # main.py
 #
 # This simulator performs the scheduling of tasks on threads in
 # OpenMP-based programs using the heuristic-based method and some of
 # the related methods.
 #**************************************************************************
 # Copyright 2023 Instituto Superior de Engenharia do Porto
 #
 # Licensed under the Apache License, Version 2.0 (the "License");
 # you may not use this file except in compliance with the License.
 # You may obtain a copy of the License at
 #
 #              http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS,
 # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 # See the License for the specific language governing permissions and
 # limitations under the License.
 #**************************************************************************
import gen
import func
import bfs
import lpt
import spt
import lnsnl
import new

# Global variables #
num_tasks = 50 # Number of tasks [random case]
bench_name = 'heat' # The name of the benchmark
et_min = 5 # Minimum execution time
et_max = 10 # Maximum execution time
et_type = 'max' # The type of execution time generation; min: Minimum, avg: Average, max: Maximum
itr = 10 # Number of iterations for execution time generation
deadline = 0 # Deadline of the system
dl_min_prob = 0.5 # Minimum probability for determining the deadline of the system
dl_max_prob = 1 # Maximum probability for determining the deadline of the system
regen_graph = False # Regenerate the graph at each iteration [random case]
dep_pro = 0.6 # Probability of selecting the sibling tasks for building the task dependency graph (TDG) [random case]
num_dep_level = 2 # Maximum number of dependencies (at each level) in the TDG [random case]
num_threads = 8 # Number of threads
graphic_result = 0 # Graphical output; 0: Not show, 1: Show

# Generate the graph #
print('The simulator uses both benchmark and random graph.')
graph_type = input("Benchmark (y) or random graph (n)? ")

if graph_type == 'y':
	# Generate it based on the benchmark #
	num_tasks, task_list = gen.graph_predef(bench_name)
else:
	# Generate it randomly #
	task_list = gen.graph_rand(num_tasks, dep_pro, num_dep_level)

print('\nThe data dependencies:')
for i in range(num_tasks):
	if len(task_list[i].dep) == 0:
		print('T' + str(task_list[i].t_id))
	else:
		dep_list = 'T' + str(task_list[i].t_id) + ' --> T' + str(task_list[i].dep[0].t_id)

		for j in range(len(task_list[i].dep))[1::]:
			dep_list += ', T' + str(task_list[i].dep[j].t_id)

		print(dep_list)

# Wait for pressing a key to continue #
print('\nPress any key to continue...')
input()

# Show the status of the mapping process #
print('The mapping is in progress...')

# Reset the file to write the results #
file = open("output/__results.dat", "w")
file.close()

# Determine execution time of tasks, deadline of the system, and generate the list of tasks #
task_list, deadline = gen.specify_et(graph_type, num_tasks, task_list, bench_name, et_min, et_max, et_type, itr, dl_min_prob, dl_max_prob)

# ++++++++++++++++++ Start the mapping with the algorithms ++++++++++++++++++++ #

results = []

# BFS algorithm #
results.append(bfs.execute(num_tasks, num_threads, func.clear(num_tasks, task_list), deadline, graphic_result))

# LPT algorithm #
results.append(lpt.execute(num_tasks, num_threads, func.clear(num_tasks, task_list), deadline, graphic_result))

# SPT algorithm #
results.append(spt.execute(num_tasks, num_threads, func.clear(num_tasks, task_list), deadline, graphic_result))

# LNSNL algorithm #
results.append(lnsnl.execute(num_tasks, num_threads, func.clear(num_tasks, task_list), deadline, graphic_result))

# NEW algorithm (MNTP, MET) #
results.append(new.execute(num_tasks, num_threads, func.clear(num_tasks, task_list), deadline, 'MNTP', 'MET', graphic_result))

# NEW algorithm (MNTP, MRT) #
results.append(new.execute(num_tasks, num_threads, func.clear(num_tasks, task_list), deadline, 'MNTP', 'MRT', graphic_result))

# NEW algorithm (MNTP, MCD) #
results.append(new.execute(num_tasks, num_threads, func.clear(num_tasks, task_list), deadline, 'MNTP', 'MCD', graphic_result))

# NEW algorithm (NT, MET) #
results.append(new.execute(num_tasks, num_threads, func.clear(num_tasks, task_list), deadline, 'NT', 'MET', graphic_result))

# NEW algorithm (NT, MRT) #
results.append(new.execute(num_tasks, num_threads, func.clear(num_tasks, task_list), deadline, 'NT', 'MRT', graphic_result))

# NEW algorithm (NT, MCD) #
results.append(new.execute(num_tasks, num_threads, func.clear(num_tasks, task_list), deadline, 'NT', 'MCD', graphic_result))

# NEW algorithm (MRIT, MET) #
results.append(new.execute(num_tasks, num_threads, func.clear(num_tasks, task_list), deadline, 'MRIT', 'MET', graphic_result))

# NEW algorithm (MRIT, MRT) #
results.append(new.execute(num_tasks, num_threads, func.clear(num_tasks, task_list), deadline, 'MRIT', 'MRT', graphic_result))

# NEW algorithm (MRIT, MCD) #
results.append(new.execute(num_tasks, num_threads, func.clear(num_tasks, task_list), deadline, 'MRIT', 'MCD', graphic_result))

# NEW algorithm (MTET, MET) #
results.append(new.execute(num_tasks, num_threads, func.clear(num_tasks, task_list), deadline, 'MTET', 'MET', graphic_result))

# NEW algorithm (MTET, MRT) #
results.append(new.execute(num_tasks, num_threads, func.clear(num_tasks, task_list), deadline, 'MTET', 'MRT', graphic_result))

# NEW algorithm (MTET, MCD) #
results.append(new.execute(num_tasks, num_threads, func.clear(num_tasks, task_list), deadline, 'MTET', 'MCD', graphic_result))

# NEW algorithm (MTRT, MET) #
results.append(new.execute(num_tasks, num_threads, func.clear(num_tasks, task_list), deadline, 'MTRT', 'MET', graphic_result))

# NEW algorithm (MTRT, MRT) #
results.append(new.execute(num_tasks, num_threads, func.clear(num_tasks, task_list), deadline, 'MTRT', 'MRT', graphic_result))

# NEW algorithm (MTRT, MCD) #
results.append(new.execute(num_tasks, num_threads, func.clear(num_tasks, task_list), deadline, 'MTRT', 'MCD', graphic_result))

# NEW algorithm (TMCD, MET) #
results.append(new.execute(num_tasks, num_threads, func.clear(num_tasks, task_list), deadline, 'TMCD', 'MET', graphic_result))

# NEW algorithm (TMCD, MRT) #
results.append(new.execute(num_tasks, num_threads, func.clear(num_tasks, task_list), deadline, 'TMCD', 'MRT', graphic_result))

# NEW algorithm (TMCD, MCD) #
results.append(new.execute(num_tasks, num_threads, func.clear(num_tasks, task_list), deadline, 'TMCD', 'MCD', graphic_result))

# Write the results to the file #
file = open("output/__results.dat", "a")

for i in range(0, 22):
	file.write(str(results[i][0]) + "\t")
	file.write(str(results[i][1]) + "\t")
	file.write(str(results[i][2]))
	if i != 21:
		file.write("\t")

file.close()
