

import os
import xml.etree.ElementTree as ET

def main():
	
	new = 'new.dat'	
	xml_name = 'GADS_ADM.xml'
	base_path = os.path.dirname(os.path.realpath(__file__))
	tree = get_xml_tree(base_path, xml_name)
	root = get_xml_root(tree)
	old_set = get_old_data(root)
	new_set = get_new_data(base_path, new)
	priority_int = highest_priority_int(root)
	diff = compute_diff(old_set, new_set)
	if diff != 'None':
		build_element(base_path, xml_name, root, diff, priority_int, tree)
	else:
		print(xml_name,'is already up to date.')


def get_xml_tree(base_path, xml_name):
	''' Parse the root from .xml file, return tree hierarchy.'''
	try:
		tree = ET.parse(os.path.join(base_path, xml_name))
		return tree
	except:
		raise FileNotFoundError (
			'Could not find xml file in current directory.'
		)

def get_xml_root(tree):
	''' Parse .xml file, return the root element for the file. '''
	_root = tree.getroot()
	return _root


def get_old_data(root):
	''' Get every line of data from the 'orgName' attribute
		in root/plugins/local/plugin/config/users
		from the .xml file. This allows for mathematical 
		comparison with the data from the LDAP server. '''
	old = set()
	try:
		for line in root.iter('orgName'):
			old.add(line.text)
		return old
	except:
		raise RuntimeError (
			'Error occured while parsing building set from xml data'
		)


def get_new_data(base_path, new_source):
	''' Get every line of data from the file containing 
		data exported from the LDAP server. 
		This data will contain attributes from AD / Catalog 
		service which needs to be included
		in the .xml file. Adding them to a set() allows for 
		mathematical comparison. '''
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
		raise RuntimeError (
			'Error occured while parsing file with new data'
		)


def highest_priority_int(root):
	''' Find the last and highest integer in attribute 
		'Priority' for every element of interest. 
		this value is later used to increase from when 
		creating new subelements in the .xml file. 
		If no previous entries are found, 0 is returned to
		start building elements from. '''
	_prio_arr = []
	highest = int()
	prio_int = root.findall(
		'plugins/local/plugin/config/users/search/priority'
	)
	if prio_int and len(prio_int) > 0:
		for elem in prio_int:
			num = int(elem.text)
			_prio_arr.append(num)
		highest = max(_prio_arr)
		return highest
	else:
		return int(0)

def compute_diff(old, new):
	''' Calculate the difference between the sets being passed 
		to this function. The sets of data contains every line 
		of text with an attribute name fetched from LDAP server 
		which is being synced to the G Suite domain. Each line 
		must be in the .xml file for to be included in the sync.
		We check if the name appears in the .xml file already by 
		comparing these two sets of data. '''
	diff = []
	try:
		for line in new:
			line = line.lstrip()
			line = line.rstrip()
			if not line in old and not '\ufeff' in line:
				diff.append(line)
		return diff if len(diff) else 'None'
	except:
		raise RuntimeError (
			'Something went wrong while building data sets for comparison'
		)


def build_element(base_path, xml_name, root, diff, prio_int, tree):
	''' Build new xml subelements for data in diff[] array passed 
		to this function. The source file is used and appended to. 
		Every 'priority' attribute is sequencially increased to 
		give elements correct priority integer with prio_int. 
		Every Element is given an identical text string in 'filter'
		attribute but with a unique ending; it's own 'orgname' text 
		string. This is used by GADS to create OU's in G Suite.	'''  
	
	_filter_string = "(&amp;(objectCategory=person)(objectClass=user)" \
					"(mail=*katrineholm.se*)(physicalDeliveryOfficeName="
	_attrib_tail = ('\n' + ('\t'*6 + ' '))
	_emlem_tail = ('\n'*2 + ('\t'*6))
	_last_attrib_tail = ('\n' + ('\t'*6))
	source_file = (os.path.join(base_path, xml_name))
	parent = root.find('plugins/local/plugin/config/users')
	try:
		for data in diff:
			prio_int += 1
			elem = ET.SubElement(parent, "search")
			elem_priority = ET.SubElement(elem, "priority")
			elem_suspended = ET.SubElement(elem, "suspended")
			elem_scope = ET.SubElement(elem, "scope")
			elem_orgname = ET.SubElement(elem, "orgName")
			elem_filter = ET.SubElement(elem, "filter")
	
			elem_priority.text = str(prio_int)
			elem_suspended.text = "false"
			elem_scope.text = "SUBTREE"
			elem_orgname.text = data
			elem_filter.text = (_filter_string + data + "))")

			elem_priority.tail = _attrib_tail
			elem_suspended.tail = _attrib_tail
			elem_scope.tail = _attrib_tail
			elem_orgname.tail = _attrib_tail
			elem_filter.tail = _attrib_tail
			elem.tail = _last_attrib_tail

		tree.write(source_file, encoding='utf-8')
		print(len(diff),'new element(s) were created.')
	except:
		raise RuntimeError (
			'Could not create new elements in file', xml_name
		)

if __name__ == '__main__':
	main()