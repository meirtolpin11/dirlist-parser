import re 
import threading
import queue
from dateutil.parser import parse
from database import DirListInfo

entity_queue = queue.Queue()

def insert_to_datebase():
	"""
		Inserting into the database
	"""
	while True:
		items = []
		maxItemsToRetrieve = 50
		for numOfItemsRetrieved in range(0, maxItemsToRetrieve):
			try:
				if numOfItemsRetrieved == maxItemsToRetrieve:
					break
				items.append(entity_queue.get_nowait())
			except:
				break

		DirListInfo.insert_many(items).execute()

def determinate_line_type(line):
	
	if "Directory of" in line:
		return 0, (line[line.find("Directory of") + len("Directory of"):].strip() + "\\").replace("\\\\", "\\")

	line = re.split('\\s+', line, maxsplit=4)

	# empty line
	if len(line) == 0:
		return -1, None

	try:
		date = parse(' '.join(line[:3]))
	except:
		return -1, None

	# if the entry is a folder 
	if line[3] == '<DIR>':
		if line[4].replace('\n', '') == '.' or line[4].replace('\n', '') == '..':
			return -1, None

		return 1, (date, line[4].replace('\n', ''))

	# if the entry is a file
	file_size = int(line[3].replace(",", ""))

	return 2, (date, file_size, line[4].replace('\n', ''))


def parse_dirlist(filename):
	current_folder = None
	entity_counter = 0
	drive = None

	with open(filename, 'r', encoding='utf-8', errors='ignore') as f:

		# ignore first 3 lines
		for _ in range(3):
			next(f)

		# start parsing the rest 
		for line in f:
			print(line)
			line_type, info = determinate_line_type(line)

			if line_type == 0:
				current_folder = info
				drive = current_folder.split(":")[0]

			elif line_type == 1:
				# a subfolder - add a line to the database 
				entity_queue.put({"computer_id" : "", "entity_drive" : drive, "entity_id" : entity_counter, "entity_root_path" : current_folder, 
					"entity_type" : 'DIR', "entity_date" : info[0], "entity_name" : info[1], "entity_size" : 0})
				entity_counter += 1

			elif line_type == 2:
				# a file - add a line to the database 
				entity_queue.put({"computer_id" : "", "entity_drive" : drive, "entity_id" : entity_counter, "entity_root_path" : current_folder, 
					"entity_type" : 'FILE', "entity_date" : info[0], "entity_name" : info[2], "entity_size" : info[1]})
				entity_counter += 1

def main():
	threading.Thread(target=insert_to_datebase, daemon=True).start()
	parse_dirlist('example.txt')
	entity_queue.join()

if __name__ == '__main__':
	main()