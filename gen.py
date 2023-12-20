 #**************************************************************************
 # gen.py
 #
 # Generate the graph based on a predefined structure or randomly,
 # as well as determine execution time of the tasks, the deadline of the
 # system, and response time of the tasks.
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
import random

# Define the task class #
class task:
	def __init__(self, t_id, et, dep, rt, status, s_time, f_time):
		self.t_id = t_id # Task ID
		self.et = et # Execution time
		self.dep = dep # The tasks list corresponding to input data dependency
		self.rt = rt # Response time of the task (only used in the new algorithms)
		self.status = status # s: Started, f : Finished
		self.s_time = s_time # Start time of the execution
		self.f_time = f_time # Finish time of the execution

# Generate the graph based on a predefined structure #
def graph_predef(bench_name):
	num_tasks = 0
	task_list = []

	# Open the file and read the contents #
	file = open("benchmark/" + bench_name + "_tdg_modified.dot", "r")
	lines = file.readlines()
	file.close()

	# Fetch the number of tasks #
	for line in lines:
		line_arr = line.strip().split("->")

		for i in range(len(line_arr)):
			if int(line_arr[i]) > num_tasks:
				num_tasks = int(line_arr[i])

	num_tasks += 1

	# Initialize the list of tasks #
	for i in range(num_tasks):
		task_list.append(task(i, None, [], None, None, None, None))

	# Specify the data dependencies #
	for line in lines:
		line_arr = line.strip().split("->")

		if len(line_arr) == 2:
			task_list[int(line_arr[1])].dep.append(task_list[int(line_arr[0])])

	return num_tasks, task_list

# Generate the graph randomly #
def graph_rand(num_tasks, dep_pro, num_dep_level):
	# Initialize the list of tasks #
	task_list = []
	for i in range(num_tasks):
		task_list.append(task(i, None, [], None, None, None, None))

	# Determine the selected list of tasks #
	sel_list = []
	for i in range(num_tasks)[1::]:
		if random.random() <= dep_pro:
			sel_list.append(task_list[i])

	# Specify data dependencies between the tasks #
	index = 0 # The pivot
	num_curr_dep = 0 # The number of current dependencies

	while num_curr_dep < len(sel_list) - 1:
		non_dep_list = [] # The non-dependent tasks in the selected list
		for i in range(len(sel_list))[index + 1::]:
			if len(sel_list[i].dep) == 0:
				non_dep_list.append(sel_list[i])

		count = 0
		for i in range(len(non_dep_list)):
			if count < num_dep_level:
				non_dep_list[i].dep.append(sel_list[index])
				count += 1
				num_curr_dep += 1
			else:
				break

		index += 1

	return task_list

# Specify execution time of the tasks, as well as calculate the deadline of the system #
# and response time of the tasks #
def specify_et(graph_type, num_tasks, task_list, bench_name, et_min, et_max, et_type, itr, dl_min_prob, dl_max_prob):
	if graph_type == 'y':
		# Determine an execution time for each task based on the json file #
		tdg_st_line_num = [] # The starting line number of each task

		# Read the json file as lines #
		with open("benchmark/" + bench_name + "_json.json") as f1:
			lines_json = f1.readlines() # Content of the file
			f1.close() # Close the file

		# Traverse the file to find the starting line number of each task #
		for i in range(num_tasks):
			for j in range(len(lines_json)):
				# Check whether the task number (i) is found in the current line #
				if (lines_json[j].find('"' + str(i) + '":') != -1):
					tdg_st_line_num.append(j) # Set the starting line number

		# Determine execution time for each task #
		for i in range(num_tasks):
			exe_list = [] # The list of execution times
			st_line_num = tdg_st_line_num[i] # The starting line number of the task

			# Specify the finishing line number of the task #
			if i != num_tasks - 1:
				fn_line_num = tdg_st_line_num[i + 1] - 1
			else:
				fn_line_num = len(lines_json) - 1

			# Find execution total times in the json and add it to the list #
			for j in range (st_line_num, fn_line_num):
				# Check whether execution total time exists in the current line #
				if (lines_json[j].find('execution_total_time') != -1):
					sp_line = lines_json[j].split(':') # Split the line
					et = int(sp_line[1].strip()) # Fetch the execution total time from the line
					exe_list.append(et) # Add the execution time to the list

			# Determine the execution time based on the minimum value #
			if et_type == 'min':
				task_list[i].et = min(exe_list)
			# Determine the execution time based on the average value #
			elif et_type == 'avg':
				task_list[i].et = round(sum(exe_list) / len(exe_list))
			# Determine the execution time based on the maximum value #
			elif et_type == 'max':
				task_list[i].et = max(exe_list)
	else:
		# Specify an execution time for each task based on a random procedure #
		for i in range(num_tasks):
			# Generate the random values #
			ran_list = []
			for j in range(itr):
				ran_list.append(random.randint(et_min, et_max))

			# Determine the execution time based on the minimum value #
			if et_type == 'min':
				task_list[i].et = min(ran_list)
			# Determine the execution time based on the average value #
			elif et_type == 'avg':
				task_list[i].et = round(sum(ran_list) / len(ran_list))
			# Determine the execution time based on the maximum value #
			elif et_type == 'max':
				task_list[i].et = max(ran_list)

	# Determine the deadline of the system #
	sum_et = 0
	for i in range(num_tasks):
		sum_et += task_list[i].et
	deadline = (random.randint(dl_min_prob * 10, dl_max_prob * 10) / 10) * sum_et

	# Calculate response time of the tasks #
	for i in range(num_tasks):
		task_list[i].rt = deadline * task_list[i].et / sum_et

	return task_list, deadline
