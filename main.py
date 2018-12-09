

import os
import xml.etree.ElementTree as ET

def main():

	# file containing new data: name
	new = 'new.dat'
	# xml file: name
	xml_name = 'GADS_ADM.xml'
	# get current filepath of execution
	base_path = os.path.dirname(os.path.realpath(__file__))
	# parse xml file for tree
	tree = get_xml_tree(base_path, xml_name)
	# parse xml file for every element in the file
	root = get_xml_root(tree)
	# fetch text data of interest from xml file to set
	old_set = get_old_data(root)
	# fetch text data of interest from text file to set
	new_set = get_new_data(base_path, new)
	# get the highest value 'priority' attribute in xml file
	priority_int = highest_priority_int(root)
	# get set containing only the data present in text file but not xml file
	diff = compute_diff(old_set, new_set)

	if diff != 'None':
		build_element(base_path, xml_name, root, diff, priority_int, tree)


def get_xml_root(tree):
	''' Parse .xml file, return the root element for the file. '''
	_root = tree.getroot()
	return _root


def get_xml_tree(base_path, xml_name):
	''' Parse the root from .xml file, return tree hierarchy.'''
	tree = ET.parse(os.path.join(base_path, xml_name))
	return tree


def get_old_data(root):
	''' Get every line of data from the 'orgName'  attribute in root/plugins/local/plugin/config/users
		from the .xml file. This allows for mathematical comparison with the data from the LDAP server.
	'''
	old = set()
	try:
		for line in root.iter('orgName'):
			old.add(line.text)
		return old
	except:
		raise RuntimeError ('Error occured while parsing building set from xml data')


def get_new_data(base_path, new_source):
	''' Get every line of data from the file containing data exported from the LDAP server. 
		This data will contain attributes from AD / Catalog service which needs to be included
		in the .xml file. Adding them to a set() allows for mathematical comparison.
	'''

	new = set()
	_new_filepath = os.path.join(base_path, new_source)
	try:
		with open(_new_filepath,'r',encoding='utf-8') as new_file:
			new_file = new_file.read().split('\n')
			for line in new_file:
				if line != '':
					new.add(line)
			return new
	except:
		raise RuntimeError ('Error occured while parsing file with new data')


def highest_priority_int(root):
	''' Find the last and highest integer in attribute 'Priority' for every element of interest. 
		this value is later used to increase from when creating new subelements in the .xml file.
	'''
	
	_prio_arr = []
	highest = int()
	# get root element for file ('filename')
	prio_int = root.findall('plugins/local/plugin/config/users/search/priority')
	for elem in prio_int:
		num = int(elem.text)
		_prio_arr.append(num)
	highest = max(_prio_arr)
	return highest


def compute_diff(old, new):
	''' Calculate the difference between the sets being passed to this function.
		The sets of data contains every line of text with an attribute name fetched from LDAP server
		which is being synced to the G Suite domain. Each line must be in the .xml file for to be included 
		in the sync. We check if the name appears in the .xml file already by comparing these two sets of data.
	'''
	diff = []
	try:
		for line in new:
			if not line in old and not '\ufeff' in line: # ignore encoding header in text file
				diff.append(line)
		if len(diff):
			return diff
		else: 
			return 'None'
	except:
		raise RuntimeError ('Something went wrong while building data sets for comparison')


def build_element(base_path, xml_name, root, diff, prio_int, tree):
	''' Build new subelements for data in diff[] array passed to this function.
		The source file is used and appended to. Every Attribute 'priority' is sequencially increased
		to give elements correct priority integer. Every Element is given an identical text string in 'filter'
		attribute but with a unique ending; it's own 'orgname' text string. This is used by GADS to create
		organizational units in G Suite.
	'''  

	_filter_string = "(&amp;(objectCategory=person)(objectClass=user)(mail=*katrineholm.se*)(physicalDeliveryOfficeName="
	
	try:
		source_file = (os.path.join(base_path, xml_name))
		parent = root.find('plugins/local/plugin/config/users')
	
		for data in diff:
			prio_int += 1
			# create attributes in new 'search' element:
			elem = ET.SubElement(parent, "search")
			elem_priority = ET.SubElement(elem, "priority")
			elem_suspended = ET.SubElement(elem, "suspended")
			elem_scope = ET.SubElement(elem, "scope")
			elem_orgname = ET.SubElement(elem, "orgName")
			elem_filter = ET.SubElement(elem, "filter")
			# contents in each attribute
			elem_priority.text = str(prio_int)
			elem_suspended.text = "false"
			elem_scope.text = "SUBTREE"
			elem_orgname.text = data
			elem_filter.text = (_filter_string + data + "))")
		tree.write(source_file, encoding='utf-8')
	except:
		raise RuntimeError ('Could not create new elements in file', xml_name)

if __name__ == '__main__':
	main()