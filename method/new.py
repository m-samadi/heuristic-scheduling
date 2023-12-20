 #**************************************************************************
 # new.py
 #
 # Map the tasks of the graph using the new mapping algorithm.
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
from operator import itemgetter
import func

# Global variables #
task_stack = [] # The task stack
alloc_queue = [] # The allocation queues of the threads
exec_queue = [] # The execution queues of the threads
curr_thr = -1 # The current thread
last_idle = [] # Last idle time of the threads (-1 for a busy thread)
comp_tasks_cnt = 0 # The number of completed tasks

alpha = 0.5
beta = 0
gamma = 0.5

theta = 0.4
psi = 0.6

# Select an allocation queue using one of the allocation heuristics #
def alloc_heuristic(num_threads, alloc_alg, t):
	global alloc_queue, curr_thr, last_idle, alpha, beta, gamma

	thr_list = [] # The thread numbers

	# The MNTP heuristic #
	if alloc_alg == 'MNTP':
		# Determine the number of tasks existing in the queues #
		for i in range(num_threads):
			thr_list.append([i, len(alloc_queue[i])])

		# Sort the numbers based on the minimum number of tasks #
		thr_list = sorted(thr_list, key = itemgetter(1), reverse = False)

		return thr_list[0][0]

	# The NT heuristic #
	elif alloc_alg == 'NT':
		# Select the next thread #
		if curr_thr < num_threads - 1:
			curr_thr += 1
		else:
			curr_thr = 0

		return curr_thr

	# The MRIT heuristic #
	elif alloc_alg == 'MRIT':
		# Calculate the recent idle time of the threads #
		for i in range(num_threads):
			if last_idle[i] != -1:
				thr_list.append([i, t - last_idle[i]])
			else:
				thr_list.append([i, 0])

		# Sort the numbers based on the most recent idle time #
		thr_list = sorted(thr_list, key = itemgetter(1), reverse = True)

		return thr_list[0][0]

	# The MTET heuristic #
	elif alloc_alg == 'MTET':
		# Calculate the total execution time of the queues #
		for i in range(num_threads):
			total_et = 0
			for j in range(len(alloc_queue[i])):
				total_et += alloc_queue[i][j].et

			thr_list.append([i, total_et])

		# Sort the numbers based on the minimum total execution time #
		thr_list = sorted(thr_list, key = itemgetter(1), reverse = False)

		return thr_list[0][0]

	# The MTRT heuristic #
	elif alloc_alg == 'MTRT':
		# Calculate the total response time of the queues #
		for i in range(num_threads):
			total_rt = 0
			for j in range(len(alloc_queue[i])):
				total_rt += alloc_queue[i][j].rt

			thr_list.append([i, total_rt])

		# Sort the numbers based on the maximum total response time #
		thr_list = sorted(thr_list, key = itemgetter(1), reverse = True)

		return thr_list[0][0]

	# The TMCD heuristic #
	elif alloc_alg == 'TMCD':
		# Calculate the recent idle time of the threads #
		rec_idle_time = []
		for i in range(num_threads):
			if last_idle[i] != -1:
				rec_idle_time.append(t - last_idle[i])
			else:
				rec_idle_time.append(0)

		# Calculate total number of tasks, total idle time, and total execution time #
		total_num_tasks = 0
		total_it = 0
		total_et = 0

		for i in range(num_threads):
			total_it += rec_idle_time[i]
			for j in range(len(alloc_queue[i])):
				total_num_tasks += 1
				total_et += alloc_queue[i][j].et

		if total_num_tasks == 0:
			total_num_tasks = 1
		if total_it == 0:
			total_it = 1
		if total_et == 0:
			total_et = 1

		# Calculate the cost of the queues #
		for i in range(num_threads):
			if rec_idle_time[i] != 0:
				val_it = 1 / (rec_idle_time[i] / total_it)
			else:
				val_it = 0

			sum_et = 0
			for j in range(len(alloc_queue[i])):
				sum_et += alloc_queue[i][j].et

			thr_list.append([i, alpha * len(alloc_queue[i]) / total_num_tasks + beta * val_it + gamma * sum_et / total_et])

		# Sort the numbers based on the least cost #
		thr_list = sorted(thr_list, key = itemgetter(1), reverse = False)

		return thr_list[0][0]

# Choose a task from the allocation queue using one of the dispatching heuristics #
def disp_heuristic(sel_tasks, disp_alg):
	global theta, psi

	# The MET heuristic #
	if disp_alg == 'MET':
		sel_id = 0
		# Find the task with the minimum execution time #
		for i in range(len(sel_tasks))[1::]:
			if sel_tasks[i].et < sel_tasks[sel_id].et:
				sel_id = i

	# The MRT heuristic #
	if disp_alg == 'MRT':
		sel_id = 0
		# Find the task with the maximum response time #
		for i in range(len(sel_tasks))[1::]:
			if sel_tasks[i].rt > sel_tasks[sel_id].rt:
				sel_id = i

	# The MCD heuristic #
	if disp_alg == 'MCD':
		# Calculate total execution time and total response time of the tasks #
		total_et = 0
		total_rt = 0
		for i in range(len(sel_tasks)):
			total_et += sel_tasks[i].et
			total_rt += sel_tasks[i].rt

		if total_et == 0:
			total_et = 1
		if total_rt == 0:
			total_rt = 1

		# Calculate the cost of each task #
		cost = []
		for i in range(len(sel_tasks)):
			cost.append(theta * sel_tasks[i].et / total_et + psi * 1 / (sel_tasks[i].rt / total_rt))

		# Select the task with the least cost #
		sel_id = 0
		for i in range(len(sel_tasks))[1::]:
			if cost[i] < cost[sel_id]:
				sel_id = i

	return sel_id

# The mapping process #
def mapping(num_tasks, num_threads, task_list, alloc_alg, disp_alg):
	global task_stack, alloc_queue, exec_queue, curr_thr, last_idle, comp_tasks_cnt

	t = 0 # Response time

	# Continue the mapping process while the allocation queues of the threads are not empty, as well as #
	# the execution queues of the threads include executing tasks #
	while comp_tasks_cnt < num_tasks:
		for thr_num in range(num_threads):
			# Check the execution queue of the thread #
			if bool(exec_queue[thr_num]):
				task = exec_queue[thr_num][len(exec_queue[thr_num]) - 1]

				# Check whether the execution of the task has been finished #
				if task.status == 's' and task.f_time <= t:
					task.status = 'f'

					curr_thr = thr_num
					last_idle[thr_num] = t
					comp_tasks_cnt += 1

			# Check the task stack and add the ready tasks to the allocation queues #
			# This process is done just by the master thread #
			if thr_num == 0:
				remove_list = []
				for i in range(len(task_stack)):
					# Add the ready tasks to the allocation queues if there are not any data dependencies, or #
					# there are any data dependencies but the related tasks are finished #
					if task_stack[i].dep == None or func.check_dep(task_list, task_stack[i].dep) == True:
						# Select an allocation queue from the list of queues #
						thread_id = alloc_heuristic(num_threads, alloc_alg, t)

						# Append the task to the selected queue #
						alloc_queue[thread_id].append(task_stack[i])

						remove_list.append(task_stack[i])

				# Remove the tasks, which were processed, from the task stack #
				for j in range(len(remove_list)):
					task_stack.remove(remove_list[j])

			# Check whether the thread is idle #
			if not bool(exec_queue[thr_num]) or exec_queue[thr_num][len(exec_queue[thr_num]) - 1].status == 'f':
				# Check the allocation queue of the thread and dispatch one of the tasks (if any) to the thread #
				if bool(alloc_queue[thr_num]):
					# Choose one of the tasks from the allocation queue #
					sel_task = alloc_queue[thr_num][disp_heuristic(alloc_queue[thr_num], disp_alg)]

					# Dispatch the task to the thread #
					exec_queue[thr_num].append(sel_task)
					task = exec_queue[thr_num][len(exec_queue[thr_num]) - 1]

					task.status = 's'
					task.s_time = t
					task.f_time = t + task.et

					last_idle[thr_num] = -1

					# Remove the task from the allocation queue #
					alloc_queue[thr_num].remove(sel_task)

		t += 1000000

	return t

# The main function #
def execute(num_tasks, num_threads, task_list, deadline, alloc_alg, disp_alg, graphic_result):
	global task_stack, alloc_queue, exec_queue, last_idle, comp_tasks_cnt

	# Create the task stack and append the tasks to this list #
	task_stack = []
	for i in range(num_tasks):
		task_stack.append(task_list[i])

	# Create an allocation queue for each thread #
	alloc_queue = []
	for i in range(num_threads):
		alloc_queue.append([])

	# Create an execution queue for each thread #
	exec_queue = []
	for i in range(num_threads):
		exec_queue.append([])

	# Create a list for the last idle time of the threads #
	last_idle = []
	for i in range(num_threads):
		last_idle.append(0)

	# Initialize the number of completed tasks #
	comp_tasks_cnt = 0

	# Show the mapping algorithm #
	print('\nNEW (' + alloc_alg + ', ' + disp_alg + ')' + '\n***********************************')
	t = mapping(num_tasks, num_threads, task_list, alloc_alg, disp_alg)

	# Calculate the results #
	response_time = t # The response time
	idle_time = sum(func.idle_time(num_threads, exec_queue, t)) # The idle time of the system
	miss_deadline = func.miss_deadline(deadline, t) # The missed deadline status of the system

	# Show the results #
	print('Response time: ' + str(response_time))
	print('Idle time: ' + str(idle_time))
	print('Missed deadline: ' + str(miss_deadline))

	# Export the scheduling of the threads #
	func.export_scheduling(num_threads, exec_queue, 'new', alloc_alg, disp_alg)

	# Draw the graphical output #
	if graphic_result == 1:
		func.graphic_result(num_threads, exec_queue, t, 'new', alloc_alg, disp_alg)

	# Return the results to the main program #
	return response_time, idle_time, miss_deadline
