
import os
import xml.etree.ElementTree as ET


def build_from_xml():

	_base_path = os.path.dirname(os.path.realpath(__file__))
		
	_xml_tree = ET.parse(os.path.join(_base_path,'GADS_adm.xml'))
	
	_subtrees = _xml_tree.getroot()
	
	_new_file_raw = open(os.path.join(_base_path,'new_file.dat'),'r',encoding = 'utf-8')
	_new_file = _new_file.readlines()

	_old_file_raw = open(os.path.join(_base_path,'old_attrib.txt',)'w',encoding = 'utf-8')
	
	# building the text file
	for pdo in _subtrees.iter('orgName'): _old_file_raw.write(pdo.text + '\n')
	_old_file = _old_file_raw.readlines()


def diff_compute():

	_new_entries = []
	_diff = []

	if not _new_file or not _subtrees:
		raise AttributeError(
			'An error occured when iterating through .xml file or attribute manifest file'
			)	
	for i in _new_file_lines: _new_entries.append(i)
	for i in _subtrees: _old_entries.append(i)

	if len(_new_entries) != len(_old_entries) and len(_new_entries) != 0:
		_new_entries.sort()
		_old_entries.sort()
		for pdo in _new_entries:
			if pdo in _old_entries:	_diff.append(pdo)

		diffstr = "".join(_diff)
		return diffstr
	else:
		return 'No data to add to new file.'

if __name__ == '__main__':
	diff_compute()

	# the_diff = diff_compute()
	# if the_diff != 'No data to add to new file.':
	# 	print('\n','>> There are new entries. These are:','\n','\n' + the_diff)
	# else:
	# 	print(the_diff)

