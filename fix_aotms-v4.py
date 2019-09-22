'''
------------------------------------------------------------------------------
Description: 
A script to fix the coordinates of specified atoms in the POSCAR format file, 
allowing to constraint the motion of these atoms during simulations in VASP.
Note that this script can only treat the situation of fixing specified layers
along z axis.
------------------------------------------------------------------------------
Author: ShuangLeung (sleung1924@gmail.com)                         
Date of last version: 2019/08/28
------------------------------------------------------------------------------
'''

import time
import os
import shutil
import linecache

print("-"*80)
starttime = time.perf_counter()
print("Starting the program at")
print(time.strftime("%Y-%m-%d %H:%M:%S"))
print("-"*80)

def fix_coordinates(filename,z0):
	# Check if the FPOSCAR file exists. If not, create a copyfile (called FPOSCAR) of POSCAR.
	if os.path.exists("FPOSCAR"):
		with open("FPOSCAR", "r+") as f:
			f.truncate()
		shutil.copyfile(os.path.join(filename),os.path.join("FPOSCAR"))

	else:
		shutil.copyfile(os.path.join(filename),os.path.join("FPOSCAR"))
	
	# Insert a new line 'Selective Dynamics' into the FPOSCAR file.
	with open("FPOSCAR") as f:
		lines = []
		for line in f:
			lines.append(line)
		lines.insert(7,'Selective Dynamics\n')
			
	with open('FPOSCAR','w') as f:
		f.writelines(lines)

	# Get the count of modified lines.
	atom_type = linecache.getline('FPOSCAR',7)
	atom_num = atom_type.split( )
	atom_tol_num = 0
	for x in atom_num:
		atom_tol_num += int(x)

	atom_line_num = 9+atom_tol_num

	# Fix the atomic coordinates.
	new_lines = []
	i = 1
	while i <= 9:
		line = linecache.getline('FPOSCAR',i)
		new_lines.append(line)
		i += 1
		while i > 9:
			line = linecache.getline('FPOSCAR',i)
			if not line:
				break
			if i <= atom_line_num :
				sp = line.split(' ')
				z = float(sp.pop())
				if z0 < z :
					add1 = line.rstrip('\n') + ' T T T\n'
					new_lines.append(add1)
				else :
					add2 = line.rstrip('\n') + ' F F F\n'
					new_lines.append(add2)
				i += 1
			else :
				break
			
	with open('FPOSCAR','w') as f:
		f.writelines(new_lines)
	
	# Print the FPOSCAR.
	with open('FPOSCAR') as f:
		print(f.read())

# Check if the POSCAR file exists. If not, enter the filename of which needed to be fixed.
if os.path.exists("POSCAR"):
	print("POSCAR file already exists, would you like import data from it?\n")
	inputstr = input("Enter 'y' to read the POSCAR.[y]\nOr enter any other character for importing data from other file.\n>>>")
	if inputstr == "y":
		print("Reading coordinate data from POSCAR...\n")
		print("Please input a z_value in a range between fix- and unfix-layer:\n")
		z_value = float(input('>>>'))
		fix_coordinates("POSCAR",z_value)
	else:
		active1 = True
		while active1:
			inputstr = input("Enter the filename of POSCAR format file containing atomic coordinates:\n>>>")
			if os.path.exists(inputstr):
				print("Reading coordinate data from %s...\n" %inputstr)
				print("Please input a z_value in a range between fix- and unfix-layer:\n")
				z_value = float(input('>>>'))
				fix_coordinates(inputstr,z_value)
				break
			else:
				print("ERROR: The input filename doesn't exist!!! Please retype the filename again.\n")
				active1 = True

else:
	active2 = True
	while active2:
		inputstr = input("Enter the filename of POSCAR format file containing atomic coordinates:\n>>>")
		if os.path.exists(inputstr):
			print("Reading coordinate data from %s...\n" %inputstr)
			print("Please input a z_value in a range between fix- and unfix-layer(z-axis coordinate):\n")
			z_value = float(input('>>>'))
			fix_coordinates(inputstr,z_value)
			break
		else:
			print("ERROR: The input filename doesn't exist!!! Please retype the filename again.\n")
			active2 = True

print("A new fix-atoms file called 'FPOSCAR' has been created! Please have a check!")

print("-"*80)
starttime = time.perf_counter()
print("Ending program at")
print(time.strftime("%Y-%m-%d %H:%M:%S"))
print("Goodbye!")
print("-"*80)
