 #**************************************************************************
 # lnsnl.py
 #
 # Map the tasks of the graph using the LNSNL heuristic presented in
 # the following paper:
 # A static scheduling approach to enable safety-critical OpenMP applications
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
import func

# Global variables #
task_stack = [] # The task stack
last_idle = [] # Last idle time of the threads (-1 for a busy thread)
thread_queue = [] # The queues of the threads
comp_tasks_cnt = 0 # The number of completed tasks

# Determine the number of outgoing dependencies #
def num_out_dep(num_tasks, task_list, curr_task):
	count = 0

	for i in range(num_tasks):
		if (task_list[i].dep != None) and (curr_task in task_list[i].dep):
			count += 1

	return count

# The mapping process #
def mapping(num_tasks, num_threads, task_list):
	global task_stack, last_idle, thread_queue, comp_tasks_cnt

	t = 0 # Response time

	# Continue the mapping process while the task stack is not empty and #
	# the queues of the threads do not include any executing tasks #
	while comp_tasks_cnt < num_tasks:
		for thr_num in range(num_threads):
			# Check the queue of each thread separately #
			if bool(thread_queue[thr_num]):
				task = thread_queue[thr_num][len(thread_queue[thr_num]) - 1]

				# The execution of the task has been finished #
				if task.status == 's' and task.f_time <= t:
					task.status = 'f'
					last_idle[thr_num] = t
					comp_tasks_cnt += 1

			# Check the task stack and dispatch the ready tasks to the threads #
			# This process is done just by the master thread, if there are any empty threads #
			if thr_num == 0 and func.check_empty_thr(num_threads, thread_queue) == True:
				if bool(task_stack):
					# Select and sort the idle threads #
					temp_idle_list = last_idle.copy()
					sort_idle_list = []

					for i in range(num_threads):
						thread_id = -1
						min_idle_time = -1

						for j in range(num_threads):
							if temp_idle_list[j] != -1:
								thread_id = j
								min_idle_time = temp_idle_list[j]
								break

						for k in range(num_threads)[j+1::]:
							if temp_idle_list[k] != -1:
								if temp_idle_list[k] < min_idle_time:
									thread_id = k
									min_idle_time = temp_idle_list[k]

						if thread_id != -1:
							sort_idle_list.append(thread_id)
							temp_idle_list[thread_id] = -1

					# Dispatch and execute the selected tasks by the idle threads #
					for index in range(len(sort_idle_list)):
						thread_id = sort_idle_list[index]

						# Select the tasks from the task stack #
						sel_tasks = []
						for i in range(len(task_stack)):
							# Select the tasks that do not have any data dependencies, #
							# or have data dependencies but the related tasks are finished #
							if task_stack[i].dep == None or func.check_dep(task_list, task_stack[i].dep) == True:
								sel_tasks.append(task_stack[i])

						# Choose one of the tasks from the selected tasks by the LNSNL heuristic #
						# Determine the number of immediate successors #
						num_successors = []
						for i in range(len(sel_tasks)):
							num_successors.append(num_out_dep(num_tasks, task_list, [sel_tasks[i]]))

						# Select the task with the largest number of immediate successors #					
						if bool(num_successors):
							max_index = 0
							max_value = num_successors[0]

							for i in range(len(num_successors))[1::]:
								if num_successors[i] > max_value:
									max_index = i
									max_value = num_successors[i]

							# Dispatch the task to the thread #
							thread_queue[thread_id].append(sel_tasks[max_index])
							task = thread_queue[thread_id][len(thread_queue[thread_id]) - 1]

							task.status = 's'
							task.s_time = t
							task.f_time = t + task.et

							last_idle[thread_id] = -1

							# Remove the task from the task stack #
							task_stack.remove(sel_tasks[max_index])

		t += 1000000

	return t

# The main function #
def execute(num_tasks, num_threads, task_list, deadline, graphic_result):
	global task_stack, last_idle, thread_queue, comp_tasks_cnt

	# Create the task stack and append the tasks to this list #
	task_stack = []
	for i in range(num_tasks):
		task_stack.append(task_list[i])

	# Create a list for the last idle time of the threads #
	last_idle = []
	for i in range(num_threads):
		last_idle.append(0)

	# Create a queue for each thread #
	thread_queue = []
	for i in range(num_threads):
		thread_queue.append([])

	# Initialize the number of completed tasks #
	comp_tasks_cnt = 0

	# Show the mapping algorithm #
	print('\nLNSNL \n***********************************')
	t = mapping(num_tasks, num_threads, task_list)

	# Calculate the results #
	response_time = t # The response time
	idle_time = sum(func.idle_time(num_threads, thread_queue, t)) # The idle time of the system
	miss_deadline = func.miss_deadline(deadline, t) # The missed deadline status of the system

	# Show the results #
	print('Response time: ' + str(response_time))
	print('Idle time: ' + str(idle_time))
	print('Missed deadline: ' + str(miss_deadline))

	# Export the scheduling of the threads #
	func.export_scheduling(num_threads, thread_queue, 'lnsnl', '', '')

	# Draw the graphical output #
	if graphic_result == 1:
		func.graphic_result(num_threads, thread_queue, t, 'lnsnl', '', '')

	# Return the results to the main program #
	return response_time, idle_time, miss_deadline
