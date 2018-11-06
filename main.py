
import os
import xml.etree.ElementTree as ET


def diff_compute(xmlsrc, newsrc):
	'''
	diff_compute takes xml file being parsed and the file containing new data as arguments.
	The data of interest in the xml file is located in elements where 'OrgName' is described. 
	The data is written to a file with encoding to preserve non-ascii characters. The data is 
	then imported as a set, to sort by unique and to allow for mathematical actions on the data.
	The temp file exported is then
	'''
	diff = []
	base_path = os.path.dirname(os.path.realpath(__file__))
	xml_tree = ET.parse(os.path.join(base_path, xmlsrc))
	subtrees = xml_tree.getroot()
	try:
		with open(os.path.join(base_path, 'old_attrib.dat'), 'w', encoding = 'utf-8') as old_file_raw:
			for data in subtrees.iter('orgName'):
				old_file_raw.write(data.text + '\n')
		
		old_file = open('old_attrib.dat', 'r', encoding = 'utf-8').read().split('\n')
		old_set = set(old_file)
		os.remove('old_attrib.dat')
		new_file = open(os.path.join(base_path, newsrc), 'r', encoding = 'utf-8').read().split('\n')
		new_set = set(new_file)
		for data in new_set:
			if not data in old_set and not '\ufeff' in data:
				diff.append(data)
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
	datablocks = []

	diff = diff_compute(xml_file, new_file)

	if not diff == 'None':
		diff_len = len(diff)
		print('\n', '* There are ',str(diff_len),' new attributes:','\n')
		for line in diff: 
			print(line, sep = ' ', end = '\n')
		# datablocks = Build(diff) >> Not built! <<

	else:
		print('No diff today - .xml file manifest is up to date.')

if __name__ == '__main__':
	main()