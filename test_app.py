from typing import List
import pytest 
from unittest import result
from app  import clean_variable , dic_json_serializable

class TestObjestDic:
	def __init__(self, name, _sa_instance_state=None):
		self.name = name
		self._sa_instance_state = _sa_instance_state

def test_clean_variable():

	value_to_test = TestObjestDic('javier', '_sa_instance_state')
	expected_result = {'name': 'javier'}
	result = clean_variable(value_to_test)
	assert result == expected_result

def test_list_json_serializable():

	value_to_test = [
		TestObjestDic(
			name='javier',
			_sa_instance_state='_sa_instance_state'
		),
		TestObjestDic(
			name='javier')
	]

	expected_result = [{"name":"javier"}, {"name":"javier"}]
	
	result = dic_json_serializable(value_to_test)
	assert result == expected_result

def test_dic_json_serializable():
	value_to_test = TestObjestDic('javier', '_sa_instance_state')
	expected_result = {'name': 'javier'}
	result = dic_json_serializable(value_to_test)
	assert result == expected_result


