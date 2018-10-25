import io
import os
import xml.etree.ElementTree as et

def diff_compute():

	_diff = []
	_origin = []
	_pdo_export = []
	_iter = None

	# establish current path
	_base_path = os.path.dirname(os.path.realpath(__file__))
	# grabbing .xml file
	_xml_file = os.path.join(_base_path, "GADS_adm.xml")
	# grabbing the manifest with all 'physicaldeliveryofficename' entries 
	_pdo_file_path = os.path.join(_base_path, "PDONoutput.txt")
	_pdo_file = io.open(_pdo_file_path, mode='r', encoding='utf-8')
	# parsing the file to get contents
	_tree = et.parse(_xml_file)
	# defining what we're looking for here. The PDO's are listed in 'orgName' children
	_root = _tree.findall(".//orgName")

	# build arrays of data for comparison
	for i in _root:
		_iter = i.text
		_origin.append(_iter)
	for n in _pdo_file:
		n = str(n)
		_pdo_export.append(n)

	for i in _origin:
		if i not in _pdo_export:
			print(i,'is not in the new file')

if __name__ == '__main__':
	diff_compute()