

import os
import xml.etree.ElementTree as ET


def get_xml_root(xml_source):
	''' Parse .xml file as source, then return the root element for
	the file.
	'''
	try:
		base_path = os.path.dirname(os.path.realpath(__file__))
		tree = ET.parse(os.path.join(base_path, xml_source))
		xml_root = tree.getroot()
		return xml_root
	except:
		raise RuntimeError ('error occured parsing .xml file for root')

def get_old_data(xmlroot):
	''' Find every 'text' attribute in 'orgname' children in the root
	being given as argument. These attributes are added to set and returned
	for comparison.
	'''
	old = set()
	try:
		for line in xmlroot.iter('orgName'):
			old.add(line.text)
		return old
	except:
		raise RuntimeError ('error occured while parsing .xml file for data')

def get_new_data(new_source):
	new = set()
	try:
		with open(new_source,'r',encoding='utf-8') as new_file:
			new_file = new_file.read().split('\n')
			for line in new_file:
				new.add(line)
			return new
	except:
		raise RuntimeError ('error occured while parsing file with new data')


# using this integer to start from, with new elements that will get created.
def highest_priority_int():
	highest = int()
	prio_arr = []
	root = get_xml_root('GADS_ADM.xml')
	prio_int = root.findall('plugins/local/plugin/config/users/search/priority')
	for elem in prio:
		num = int(elem.text)
		prio_arr.append(num)
	highest = max(prio_arr)
	return highest


# calculate diff between the new and old sets
def compute_diff():
	diff = []
	root = get_xml_root('GADS_ADM.xml')
	old_set = get_old_data(root)
	new_set = get_new_data('new.dat')
	try:
		for line in new_set:
			if not line in old_set and not '\ufeff' in line:
				diff.append(line)
		if len(diff) >= 1:
			return diff
		else: 
			return 'None'
	except:
		raise RuntimeError ('Fatal error: something went wrong while building data sets of files')


def build_element(diff):
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

	diff = compute_diff()

	if diff != 'None':
		# datablocks = build(diff) >> Not built! <<
		for line in diff:
			print(line)
	else:
		print('No diff today - XML file is up to date.')

if __name__ == '__main__':
	main()
