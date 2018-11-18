
import os
import xml.etree.ElementTree as ET

def diff_compute(xmlsrc, newsrc):
	'''
	diff_compute takes xml file being parsed and the file containing new data as arguments.
	The data of interest in the xml file is located in elements where 'OrgName' is described. 
	The data is added to set, as will every line from the .dat fiile containing the new data. 
	The sets are compared and differing values are added to diff[] and returned.
	'''
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


def main():
	# define names for the .xml file to parse and the dat file with new attributes to compare with
	xml_file = 'GADS_ADM.xml'
	new_file = 'new.dat'
	diff_len = 0
	diff = diff_compute(xml_file, new_file)

	if diff != 'None':
		diff_len = len(diff)
		print('\n', '* There are',str(diff_len),'new attributes:','\n')
		for line in diff: 
			print(line, sep = ' ', end = '\n')
		# datablocks = build(diff) >> Not built! <<
	else:
		print('No diff today - .xml file manifest is up to date.')

if __name__ == '__main__':
	main()

def build(diff)
	
	# for every line of text in diff[]:
		# line is part of xml element, attribute orgName
		# xml element has attributes

	# Find highest integer '<priority>' in the list of .xml elements with 'search' parent
	# int(priority) += 1

	# With every block of xml code for every line in diff[]:
		# add to source file
		# save source file

	# verify correctly saved data