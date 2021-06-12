
import warnings
import unittest
import boto3
import sys
from moto import mock_dynamodb2
sys.path.insert(1, 'src/utils/')

@mock_dynamodb2
class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
		warnings.filterwarnings(
			"ignore",
			category=ResourceWarning,
			message="unclosed.*<socket.socket.*>")
		warnings.filterwarnings(
			"ignore",
			category=DeprecationWarning,
			message="callable is None.*")
		warnings.filterwarnings(
			"ignore",
			category=DeprecationWarning,
			message="Using or importing.*")
		"""Create the mock database and table"""
		self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
		self.uuid = "123e4567-e89b-12d3-a456-426614174000"
		self.text = "Aprender DevOps y Cloud en la UNIR"

		from todoTableClass import todoTableClass
		self.table_handler_a = todoTableClass("todoTableClasslocal")
		self.table_a = self.table_handler_a.create_todo_table()
		self.table_handler_b = todoTableClass("todoTableClasslocal", self.dynamodb)
		self.table_b = self.table_handler_b.create_todo_table()

    def tearDown(self):
		"""Delete mock database and table after test is run"""
		self.table_handler_a.delete_todo_table()
		self.table_handler_b.delete_todo_table()
		del self.table_handler_a
		del self.table_handler_b
		
		self.dynamodb = None
	
    def test_table_exists(self):
		self.assertTrue(self.table_a) # verificamos si la tabla existe
		self.assertTrue(self.table_b) # verificamos si la tabla existe
		# verificamos si el nombre de la tabla es ToDo
		self.assertIn('todoTableClasslocal', self.table_a.name)
		self.assertIn('todoTableClasslocal', self.table_b.name)
		# pprint(self.table.name)
	
    def test_put_todo(self):
		# Haciendo pruebas a la clase todoTableClass
		# Tabla a local
		self.assertEqual(200, self.table_handler_a.put_todo(
			self.text, self.uuid)['statusCode'])
		# Tabla b mockeada
		self.assertEqual(
			200,
			self.table_handler_b.put_todo(
			self.text,
			self.uuid)['statusCode'])

    def test_put_todo_error(self):
		# Haciendo pruebas a la clase todoTableClass
		# Tabla a local
		self.assertRaises(
			Exception,
			self.table_handler_a.put_todo(
				"",
				self.uuid))
		self.assertRaises(Exception, self.table_handler_a.put_todo("", ""))
		self.assertRaises(
			Exception,
			self.table_handler_a.put_todo(
				self.text,
				""))
		# Tabla b mockeada
		self.assertRaises(
			Exception, self.table_handler_b.put_todo("", self.uuid))
		self.assertRaises(
			Exception, self.table_handler_b.put_todo("",""))
		self.assertRaises(
			Exception, self.table_handler_b.put_todo(self.text,""))

	def test_get_todo(self):
		# Haciendo pruebas a la clase todoTableClass
		# Tabla a local
		self.table_handler_a.put_todo(self.text, self.uuid)
		self.assertEqual(200, self.table_handler_a.get_todo(
			self.uuid)['ResponseMetadata']['HTTPStatusCode'])
		self.assertEqual(
			self.text, self.table_handler_a.get_todo(
				self.uuid)['Item']['text'])
		
		# Tabla b mockeada
		self.table_handler_b.put_todo(self.text, self.uuid)
		self.assertEqual(200, self.table_handler_b.get_todo(
			self.uuid)['ResponseMetadata']['HTTPStatusCode'])
		self.assertEqual(
			self.text,
			self.table_handler_b.get_todo(self.uuid)['Item']['text'])

	def test_get_todo_error(self):
		














