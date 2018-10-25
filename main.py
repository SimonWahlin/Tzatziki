
import os
import xml.etree.ElementTree as et

def diff_compute():

	diffstr = None
	_new_entries = []
	_old_entries = []
	_diff = []

	# establish current path
	_base_path = os.path.dirname(os.path.realpath(__file__))
	# grabbing the manifest with all 'physicaldeliveryofficename' entries 
	_pdo_file = open(os.path.join(_base_path,'PDONoutput.txt'),'r',encoding = 'utf-8')
	# grabbing .xml file
	_xml_file = os.path.join(_base_path,'GADS_adm.xml')
	# parsing the file to get contents
	_tree = et.parse(_xml_file)
	# defining what we're looking for here. The PDO's are listed in 'orgName' children
	_subtrees = _tree.findall(".//orgName")
	
	if not _pdo_file or not _subtrees:
		raise AttributeError(
			'An error occured when iterating through .xml file or attribute manifest file'
			)	
	for i in _pdo_file: _new_entries.append(i)
	for i in _subtrees: _old_entries.append(i.text)

	if len(_new_entries) != len(_old_entries) and len(_new_entries) != 0:
		_new_entries.sort()
		_old_entries.sort()
		for pdo in _new_entries:
			if not pdo in _old_entries:	_diff.append(pdo)

		diffstr = "".join(_diff)
		return diffstr
	else:
		return 'No data to add to new file.'

if __name__ == '__main__':
	the_diff = diff_compute()
	if the_diff != 'No data to add to new file.':
		print('\n','>> There are new entries. These are:','\n','\n' + the_diff)
	else:
		print(the_diff)