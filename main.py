
import os
import xml.etree.ElementTree as ET

def compute_diff(xmlsrc, newsrc):

	old = set()
	new = set()
	diff = []

	base_path = os.path.dirname(os.path.realpath(__file__))
	tree = ET.parse(os.path.join(base_path, xmlsrc))
	root = tree.getroot()
	
	try:
		new_file = open(newsrc,'r',encoding='utf-8').read().split('\n')
		for line in new_file: new.add(line)
		del new_file
		for line in root.iter('orgName'):
			old.add(line.text)
		for line in new:
			if not line in old and not '\ufeff' in line:
				diff.append(line)
		if diff and len(diff) > 1: 
			return diff
		else: 
			return 'None'
	except:
		raise RuntimeError ('Fatal error: something went wrong while building data sets of files')


def find_highest_priority():

	pass
	# find the highest integer in <priority> for every child parsed
	# return integer +1 to start building from.
	# root.findall('plugins/local/plugin/config/users/search/priority')


def build_element(diff)
	
	pass
	# for every line of text in diff[]:
		# line is part of xml element, attribute orgName
		# xml element has attributes

	# Find highest integer '<priority>' in the list of .xml elements with 'search' parent
	# int(priority) += 1

	# With every block of xml code for every line in diff[]:
		# add to source file
		# save source file

	# verify correctly saved data


def main():
	# define names for the .xml file to parse and the dat file with new attributes to compare with
	xml_file = 'GADS_ADM.xml'
	new_file = 'new.dat'
	diff = compute_diff(xml_file, new_file)

	if diff != 'None':
		# datablocks = build(diff) >> Not built! <<
	else:
		print('No diff today - XML file is up to date.')

if __name__ == '__main__':
	main()
