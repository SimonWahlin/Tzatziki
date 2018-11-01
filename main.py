
import os
import xml.etree.ElementTree as ET


def diff_compute(xml,newfile):
	diff = []
	_base_path = os.path.dirname(os.path.realpath(__file__))
	_xml_tree = ET.parse(os.path.join(_base_path,xml))
	_subtrees = _xml_tree.getroot()

	try:
		# building dat file with old attributes from the .xml file
		_old_file_raw = open(os.path.join(_base_path,'old_attrib.dat'),'w',encoding = 'utf-8')
		for pdo in _subtrees.iter('orgName'): _old_file_raw.write(pdo.text + '\n')
		_old_file_raw.close()
		
		_old_file_raw = open(os.path.join(_base_path,'old_attrib.dat'),'r',encoding = 'utf-8')
		_old_file = _old_file_raw.readlines()
		_old_file_raw.close()
	except:
		raise RuntimeError ('An error occured with generating the .dat file from .xml data. Verify permissions and access.')
	try:
		# opening dat file with new attributes
		_new_file_raw = open(os.path.join(_base_path,newfile),'r',encoding = 'utf-8')
		_new_file = _new_file_raw.readlines()
		_new_file_raw.close()
	except:
		if not _new_file or not _old_file: 
			raise RuntimeError ('An error occured. Is the .xml file and new attrib file there?')

	for pdo in _new_file:
		if not pdo in _old_file:
			diff.append(pdo)

	if diff and len(diff) > 1: 
		return diff
	else: 
		return 'None'



def main():

	diff_len = 0
	diff = diff_compute('GADS_ADM.xml','new_attrib.dat')

	if not diff == 'None':
		diff_len = len(diff)
		print('There are ',str(diff_len),' new attributes:','\n')
		print(diff)
	else:
		print('No diff today - .xml file manifest is up to date.')

	# Build .xml data blocks for each new entry. must resemble data block found in orgName children in GADS file.
	# Requires numeric counter for every block of data, later used as '<priority>' in xml.


if __name__ == '__main__':
	main()