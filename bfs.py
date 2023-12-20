 #**************************************************************************
 # bfs.py
 #
 # Map the tasks of the graph using the breadth-first scheduler (BFS).
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
thread_queue = [] # The queues of the threads
curr_thread_num = -1 # The thread number of the last finished task
comp_tasks_cnt = 0 # The number of completed tasks

# Find an idle thread #
def find_idle_thread(num_threads, thread_queue, curr_thread_num):
	thread_num = None

	# If the number of threads is less than or equal to 2 #
	if num_threads <= 2:
		if curr_thread_num == 0:
			for i in range(num_threads)[::-1]:
				if not bool(thread_queue[i]) or thread_queue[i][len(thread_queue[i]) - 1].status == 'f':
					thread_num = i
					break			
		else:
			for i in range(num_threads)[::]:
				if not bool(thread_queue[i]) or thread_queue[i][len(thread_queue[i]) - 1].status == 'f':
					thread_num = i
					break				

	# If the number of threads is more than 2 #
	else:
		if curr_thread_num != num_threads - 1:
			for i in range(num_threads)[curr_thread_num + 1::]:
				if not bool(thread_queue[i]) or thread_queue[i][len(thread_queue[i]) - 1].status == 'f':
					thread_num = i
					break

			if thread_num == None:
				for i in range(num_threads)[:curr_thread_num:]:
					if not bool(thread_queue[i]) or thread_queue[i][len(thread_queue[i]) - 1].status == 'f':
						thread_num = i
						break
		else:
			for i in range(num_threads):
				if not bool(thread_queue[i]) or thread_queue[i][len(thread_queue[i]) - 1].status == 'f':
					thread_num = i
					break

	return thread_num

# The mapping process #
def mapping(num_tasks, num_threads, task_list):
	global task_stack, thread_queue, curr_thread_num, comp_tasks_cnt

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
					curr_thread_num = thr_num
					comp_tasks_cnt += 1

			# Check the task stack and dispatch the ready tasks to the threads #
			# This process is done just by the master thread, if there are any empty threads #
			if thr_num == 0 and func.check_empty_thr(num_threads, thread_queue) == True:
				if bool(task_stack):
					remove_list = []
					# Look for any tasks in the task stack and find an idle thread for each task #
					for i in range(len(task_stack)):
						# Dispatch the task to a thread if there are not any data dependencies, or #
						# there are any data dependencies but the related tasks are finished #
						if task_stack[i].dep == None or func.check_dep(task_list, task_stack[i].dep) == True:
							# Find an idle thread for the task #
							thread_num = find_idle_thread(num_threads, thread_queue, curr_thread_num)

							# An idle thread is found #
							if thread_num != None:
								thread_queue[thread_num].append(task_stack[i])
								new_task = thread_queue[thread_num][len(thread_queue[thread_num]) - 1]

								new_task.status = 's'
								new_task.s_time = t
								new_task.f_time = t + task_stack[i].et

								remove_list.append(task_stack[i])

					# Remove the tasks, which were processed, from the task stack #
					for j in range(len(remove_list)):
						list_index = task_stack.index(remove_list[j])
						task_stack.remove(task_stack[list_index])

		t += 1000000

	return t

# The main function #
def execute(num_tasks, num_threads, task_list, deadline, graphic_result):
	global task_stack, thread_queue, comp_tasks_cnt

	# Create the task stack and append the tasks to this list #
	task_stack = []
	for i in range(num_tasks):
		task_stack.append(task_list[i])

	# Create a queue for each thread #
	thread_queue = []
	for i in range(num_threads):
		thread_queue.append([])

	# Initialize the number of completed tasks #
	comp_tasks_cnt = 0

	# Show the mapping algorithm #
	print('\nBFS \n***********************************')
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
	func.export_scheduling(num_threads, thread_queue, 'bfs', '', '')

 	# Draw the graphical output #
	if graphic_result == 1:
		func.graphic_result(num_threads, thread_queue, t, 'bfs', '', '')

	# Return the results to the main program #
	return response_time, idle_time, miss_deadline
