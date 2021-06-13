
import warnings
import unittest
import boto3
import sys
from todoTableClass import todoTableClass
from moto import mock_dynamodb2
sys.path.insert(1, 'src/utils/')

@mock_dynamodb2
class TestDatabaseFunctions(unittest.TestCase):
	
	# Metodo que se ejecuta antes de cada funcion test: creamos bd y tablas
	def setUp(self):
		warnings.filterwarnings("ignore",
								category=ResourceWarning,
								message="unclosed.*<socket.socket.*>")
		warnings.filterwarnings("ignore",
								category=DeprecationWarning,
								message="callable is None.*")
		warnings.filterwarnings("ignore",
								category=DeprecationWarning,
								message="Using or importing.*")
		
		# Datos de la bd y tabla mockeada de prueba
		self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
		self.uuid = "123e4567-e89b-12d3-a456-426614174000"
		self.text = "Aprender DevOps y Cloud en la UNIR"

		# Crea tabla en dynamodb docker local 
		self.table_handler_a = todoTableClass()
		self.table_handler_a.set_table_name("todoTableClasslocal")
		self.table_a = self.table_handler_a.create_todo_table()
		
		# Crea tabla en dynamodb AWS mockeado
		self.table_handler_b = todoTableClass(self.dynamodb)
		self.table_handler_b.set_table_name("todoTableClasslocal")
		self.table_b = self.table_handler_b.create_todo_table()

	# Metodo que se ejecuta despues de cada funcion test: limpiamos bd y tablas
    def tearDown(self):
		self.table_handler_a.delete_todo_table()
		self.table_handler_b.delete_todo_table()
		del self.table_handler_a
		del self.table_handler_b
		self.dynamodb = None
	
    def test_table_exists(self):
		self.assertTrue(self.table_a) # verificamos si la tabla existe
		self.assertTrue(self.table_b) # verificamos si la tabla existe
	
		self.assertIn('todoTableClasslocal', self.table_a.name)
		self.assertIn('todoTableClasslocal', self.table_b.name)
	
	########################## FUNCIONES DE PRUEBA #################################
	# Verificamos la funcion get_todo(): Casos en que debe retornar OK
	def test_get_todo(self):
		# Tabla a local
		self.table_handler_a.put_todo(self.text, self.uuid) # Primero agregamos un registro
		# Probamos que el metodo get retorne OK y devuelva el texto esperado
		self.assertEqual(200,
			self.table_handler_a.get_todo(self.uuid)['ResponseMetadata']['HTTPStatusCode'])
		self.assertEqual(self.text,
			self.table_handler_a.get_todo(self.uuid)['Item']['text'])
		
		# Tabla b mockeada
		self.table_handler_b.put_todo(self.text, self.uuid) # Primero agregamos un registro
		# Probamos que el metodo get retorne OK y devuelva el texto esperado
		self.assertEqual(200,
			self.table_handler_b.get_todo(self.uuid)['ResponseMetadata']['HTTPStatusCode'])
		self.assertEqual(self.text,
			self.table_handler_b.get_todo(self.uuid)['Item']['text'])

	# Verificamos la funcion get_todo(): Casos en que debe retornar error
	def test_get_todo_error(self):
		# Tabla a local
		self.table_handler_a.put_todo(self.text, self.uuid) # Primero agregamos un registro
		self.assertRaises(Exception, self.table_handler_a.get_todo("") # El método debe retornar error 
		self.assertRaises(Exception, self.table_handler_a.get_todo("ID-INEXISTENTE") # El método debe retornar error
		
		# Tabla b mockeada
		self.table_handler_b.put_todo(self.text, self.uuid) # Primero agregamos un registro
		self.assertRaises(Exception, self.table_handler_b.get_todo("") # El método debe retornar error 
		self.assertRaises(Exception, self.table_handler_b.get_todo("ID-INEXISTENTE") # El método debe retornar error
	
	# Verificamos la funcion scan_todo(): Casos en que debe retornar OK
	def test_scan_todo(self):
		# Tabla a local
		self.table_handler_a.put_todo(self.text, self.uuid) # Primero agregamos un registro
		# Probamos que el metodo get retorne OK y devuelva el texto esperado
		self.assertEqual(200,
			self.table_handler_a.scan_todo()['ResponseMetadata']['HTTPStatusCode'])
		# self.assertEqual(self.text,
		#  	 self.table_handler_a.scan_todo()['Items'][0]['text'])
		
		# Tabla b mockeada
		self.table_handler_b.put_todo(self.text, self.uuid) # Primero agregamos un registro
		# Probamos que el metodo get retorne OK y devuelva el texto esperado
		self.assertEqual(200,
			self.table_handler_a.scan_todo()['ResponseMetadata']['HTTPStatusCode'])
	
	# Verificamos la funcion update_todo(): Casos en que debe retornar OK
	def test_update_todo(self):
		# Tabla a local
		self.table_handler_a.put_todo(self.text, self.uuid) # Primero agregamos un registro
		# Probamos que el metodo update retorne OK y devuelva el texto esperado
		self.assertEqual(200,
			self.table_handler_a.update_todo('Lambda es increible', self.uuid, true)['ResponseMetadata']['HTTPStatusCode'])
		# Verificamos que los datos se hayan cambiado
		self.assertEqual(self.table_handler_a.get_todo(self.uuid)['Item']['text'], 'Lambda es increible')
		self.assertEqual(self.table_handler_a.get_todo(self.uuid)['Item']['checked'], true)
	
		# Tabla b mockeada
		self.table_handler_b.put_todo(self.text, self.uuid) # Primero agregamos un registro
		# Probamos que el metodo update retorne OK y devuelva el texto esperado
		self.assertEqual(200,
			self.table_handler_b.update_todo('Lambda es increible', self.uuid, true)['ResponseMetadata']['HTTPStatusCode'])
		# Verificamos que los datos se hayan cambiado
		self.assertEqual(self.table_handler_b.get_todo(self.uuid)['Item']['text'], 'Lambda es increible')
		self.assertEqual(self.table_handler_b.get_todo(self.uuid)['Item']['checked'], true)
	
	# Verificamos la funcion put_todo(): Casos en que debe retornar OK
    def test_put_todo(self):
		# Ejecución en Tabla a local debe retornar 200(OK)
		self.assertEqual(200, self.table_handler_a.put_todo(self.text,self.uuid)['statusCode'])
		# Ejecución en Tabla b mockeada debe retornar 200(OK)
		self.assertEqual(200, self.table_handler_b.put_todo(self.text,self.uuid)['statusCode'])

	# Verificamos la funcion put_todo(): Casos en que debe retornar error
    def test_put_todo_error(self):
		# Tabla a local
		# self.assertRaises(Exception, self.table_handler_a.put_todo("", self.uuid))
		self.assertRaises(Exception, self.table_handler_a.put_todo("", ""))
		self.assertRaises(Exception, self.table_handler_a.put_todo(self.text,""))
		
		# Tabla b mockeada
		# self.assertRaises(Exception, self.table_handler_b.put_todo("", self.uuid))
		self.assertRaises(Exception, self.table_handler_b.put_todo("",""))
		self.assertRaises(Exception, self.table_handler_b.put_todo(self.text,""))

	# Verificamos la funcion delete_todo(): Casos en que debe retornar OK
    def test_delete_todo(self):
    	self.table_handler_a.put_todo(self.text, self.uuid) # Primero agregamos un registro
		# Ejecución en Tabla a local debe retornar 200(OK)
		self.assertEqual(200, self.table_handler_a.delete_todo(self.uuid)['statusCode'])
		
		self.table_handler_b.put_todo(self.text, self.uuid) # Primero agregamos un registro
		# Ejecución en Tabla b mockeada debe retornar 200(OK)
		self.assertEqual(200, self.table_handler_b.delete_todo(self.uuid)['statusCode'])
	
	# Verificamos la funcion translate_todo(): Casos en que debe retornar OK
    def test_translate_todo(self):
    	self.table_handler_a.put_todo(self.text, self.uuid) # Primero agregamos un registro
    	# Ejecución en Tabla a local debe retornar 200(OK)
		self.assertEqual(200, self.table_handler_a.translate_todo(self.uuid,'es','en')['statusCode'])
		self.assertEqual(self.table_handler_a.translate_todo(self.uuid,'es','en')['Item']['TranslatedText'], "Learn DevOps and Cloud at UNIR")
		
		self.table_handler_b.put_todo(self.text, self.uuid) # Primero agregamos un registro
		# Ejecución en Tabla b mockeada debe retornar 200(OK)
		self.assertEqual(200, self.table_handler_b.translate_todo(self.uuid,'es','en')['statusCode'])
		self.assertEqual(self.table_handler_b.translate_todo(self.uuid,'es','en')['Item']['TranslatedText'], "Learn DevOps and Cloud at UNIR")
	
	