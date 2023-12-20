 #**************************************************************************
 # func.py
 #
 # This file includes the common functions that are used by different files.
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
from PIL import Image, ImageDraw, ImageFont

# Clear the detailed contents of the tasks #
def clear(num_tasks, task_list):
	for i in range(num_tasks):
		task_list[i].status = None
		task_list[i].s_time = None
		task_list[i].f_time = None

	return task_list

# Check for existing empty threads #
def check_empty_thr(num_threads, thread_queue):
	flag_empty = False

	for i in range(num_threads):
		if not bool(thread_queue[i]):
			flag_empty = True
		else:
			if thread_queue[i][len(thread_queue[i]) - 1].status == 'f':
				flag_empty = True

	return flag_empty

# Check meeting the dependencies #
def check_dep(task_list, dep_list):
	flag_finished = True

	for i in range(len(dep_list)):
		for j in range(len(task_list)):
			if dep_list[i] == task_list[j] and task_list[j].status != 'f':
				flag_finished = False

	return flag_finished

# Calculate the idle times of the threads #
def idle_time(num_threads, queue, t):
	idle_time_thr = [] # Idle time of each thread

	# Determine the idle time of each thread #
	for i in range(num_threads):
		idle_time_thr.append([])

		# Check the queue of the thread #
		# The queue is empty #
		if len(queue[i]) == 0:
			idle_time_thr[i] = t
		# The queue is not empty #
		else:
			for j in range(len(queue[i])):
				if j == 0:
					idle_time_thr[i] = queue[i][j].s_time - 1
				else:
					if queue[i][j].s_time != queue[i][j - 1].f_time:
						idle_time_thr[i] += queue[i][j].s_time - queue[i][j - 1].f_time - 1

				if j == len(queue[i]) - 1:
					idle_time_thr[i] += t - queue[i][j].f_time

	return idle_time_thr

# Specify the missed deadline status of the system #
def miss_deadline(deadline, t):
	if t <= deadline:
		return 0
	else:
		return 1

# Export the scheduling of the threads to the files #
def export_scheduling(num_threads, queue, alg_name, par1, par2):
	# Create the output file #
	if alg_name == 'bfs':
		file = open("output/bfs_scheduling.dat", "w")
	elif alg_name == 'lpt':
		file = open("output/lpt_scheduling.dat", "w")
	elif alg_name == 'spt':
		file = open("output/spt_scheduling.dat", "w")
	elif alg_name == 'lnsnl':
		file = open("output/lnsnl_scheduling.dat", "w")
	elif alg_name == 'new':
		file = open("output/new_" + par1 + "_" + par2 + "_scheduling.dat", "w")

	for i in range(num_threads):
		# Write the name of the thread #
		file.write('Thr' + str(i) + ':\n')

		# Write the name of each task executed by the thread #
		for j in range(len(queue[i])):
			file.write('T' + str(queue[i][j].t_id) + "\n")

		if i != num_threads - 1:
			file.write("\n")

	file.close()

# Draw the graphical result #
def graphic_result(num_threads, queue, t, alg_name, par1, par2):
	# Specify the width of the window, the height of the queues, and the height of the window #
	win_width = num_threads * 100 + (num_threads - 1) * 10 + 100 # The width of the window
	queue_height = t # The height of the queues
	win_height = queue_height * 10 + 100 # The height of the window

	# Prepare the drawing process #
	im = Image.new('RGB', (win_width, win_height), (255, 255, 255))
	draw = ImageDraw.Draw(im)

	# Draw the name and contents of each thread #
	l_point = 50
	font_thr_id = ImageFont.truetype(r'C:\Users\System-Pc\Desktop\arial.ttf', 20) 
	font_task_id = ImageFont.truetype(r'C:\Users\System-Pc\Desktop\arial.ttf', 15)

	for i in range(num_threads):
		# Draw the name of the thread #
		thr_id = 'Thr' + str(i)
		draw.text((l_point + 25, 20), thr_id, fill = "black", font = font_thr_id, align = "center")

		# Draw the main box of the thread #
		draw.rectangle((l_point, 50, l_point + 100, queue_height * 10 + 60), fill = (255, 255, 255), outline = (0, 0, 0), width = 2)

		for j in range(len(queue[i])):
			# Draw the box related to the execution of each task #
			draw.rectangle((l_point, queue[i][j].s_time * 10 + 50, l_point + 100, queue[i][j].f_time * 10 + 50), fill = (0, 255, 0), outline = (0, 0, 0), width = 1)
			# Draw the name of the task #
			task_id = 'T' + str(queue[i][j].t_id)
			draw.text((l_point + 40, (queue[i][j].s_time + (queue[i][j].f_time - queue[i][j].s_time) // 2) * 10 + 45), task_id, fill = "black", font = font_task_id, align = "center")

		l_point += 110

	# Create the output file #
	if alg_name == 'bfs':
		im.save('output/bfs.jpg', quality = 300)
	elif alg_name == 'lpt':
		im.save('output/lpt.jpg', quality = 300)
	elif alg_name == 'spt':
		im.save('output/spt.jpg', quality = 300)
	elif alg_name == 'lnsnl':
		im.save('output/lnsnl.jpg', quality = 300)
	elif alg_name == 'new':
		im.save('output/new_' + par1 + '_' + par2 + '.jpg', quality = 300)
