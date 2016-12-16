# Python script to split motion jpeg file into many jpeg files.

import sys
import os

# Handle arguments
input_filename = ""
out_dir = "out"

if len(sys.argv) == 2:
	input_filename = sys.argv[1]
elif len(sys.argv) == 3:
	input_filename = sys.argv[1]
	out_dir = sys.argv[2]
else:
	print 'Usage: python split_mjpg.py <mjpg file> [<out dir>]'
	exit(0)
	
print "Input file:", input_filename
print "Output Directory:", out_dir

# open input file
f = open(input_filename, 'rb')

# open first output file
if not os.path.isdir(out_dir):
	os.mkdir(out_dir)
	print "Make directory %s"%out_dir

def open_next_jpg_file():
	open_next_jpg_file.index = open_next_jpg_file.index + 1
	filename = "%s\\%03d.jpg"%(out_dir, open_next_jpg_file.index)
	fo = open(filename, "wb")
	print "Write", filename
	return fo
	
open_next_jpg_file.index = 0
fo = open_next_jpg_file()

# read first byte
byte = f.read(1)
last_byte = byte

# process all following bytes, one by one
while byte != b"":
	fo.write(byte)
	
	# check FF D9 FF D8 pattern
	if last_byte == b'\xff':
		if byte == b'\xd9':
			b1 = f.read(1)
			b2 = f.read(1)
			f.seek(-2, 1)
			
			if b1 == b'\xff' and b2 == b'\xd8':
				# reopen file
				fo.close()
				fo=open_next_jpg_file()
			
			# if eof, exit
			if b1 == b"":
				fo.close()
				break
	
	last_byte = byte 
	byte = f.read(1)
	
print "Completed!"
