
import os
import xml.etree.ElementTree as ET

def diff_compute():

	diffstr = None
	_new_entries = []
	_old_entries = []
	_diff = []

	# establish current path
	_base_path = os.path.dirname(os.path.realpath(__file__))
	
	# grabbing the manifest with all 'physicaldeliveryofficename' entries 
	_pdo_file = open(os.path.join(_base_path,'PDONoutput.txt'),'r',encoding = 'utf-8')
		
	# parsing the file to get contents
	_tree = ET.parse(os.path.join(_base_path,'GADS_adm.xml'))
	_outfile = file.write(os.path.join(_base_path,''))
	# defining what we're looking for here. The PDO's are listed in 'orgName' children
	_subtrees = _tree.getroot()
	
	for orgname in _subtrees.iter('orgName'):
		i = str(orgname.text)
		

	for orgname in _pdo_file.iter():
		if orgname in _old_entries:
			print(orgname)
		else:
			print('no match')

	# if not _pdo_file or not _subtrees:
	# 	raise AttributeError(
	# 		'An error occured when iterating through .xml file or attribute manifest file'
	# 		)	
	# for i in _pdo_file_lines: _new_entries.append(i)
	# for i in _subtrees: _old_entries.append(i)

	# if len(_new_entries) != len(_old_entries) and len(_new_entries) != 0:
	# 	_new_entries.sort()
	# 	_old_entries.sort()
	# 	for pdo in _new_entries:
	# 		if pdo in _old_entries:	_diff.append(pdo)

	# 	diffstr = "".join(_diff)
	# 	return diffstr
	# else:
	# 	return 'No data to add to new file.'

if __name__ == '__main__':
	diff_compute()

	# the_diff = diff_compute()
	# if the_diff != 'No data to add to new file.':
	# 	print('\n','>> There are new entries. These are:','\n','\n' + the_diff)
	# else:
	# 	print(the_diff)