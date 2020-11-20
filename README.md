# AWSDynamoDB

Esta proyecto hace un empaquetamiento para el uso del servicio AWS de dynamodb

## Consideraciones
  - Se debe contar con una cuenta de AWS para su uso
  - Para el manejo de ambientes se utiliza un archivo .en con la siguinte estructura:
  ```
  # Production credentials
  PROD_AWS_ACCESS_KEY_ID =
  PROD_AWS_SECRET_ACCESS_KEY =
  PROD_AWS_REGION =

  # Development credentials
  DEV_AWS_ACCESS_KEY_ID =
  DEV_AWS_SECRET_ACCESS_KEY =
  DEV_AWS_REGION =

  ```
  - el desarrollador debe saber el nombre de la tabla sobre la que trabajara
  - el desarrollador debe saber el schema de la tabla de dynamodb, en caso de no conocerlo
    existe una forma de poder obtenerlo.
## Funcionalidades
 - Iniciar conexion a DDB
 ``` python
  from aws_dynamodb import AWSDynamoDB
  client = AWSDynamoDB() # se puede indicar el ambiente utilizando el attr env, por defecto es development
 ```
 
 - Seleccionar tabla 
 ``` python
 client.set_table_name("Test")

 ```
 
 - Conocer squema de la tabla
 ``` python
 print(client.get_table_schema())

 ```
 
 - Insertar o actualizar elemento en DDB, teniendo el schema claro este puede ser un ejemplo
 ``` python
 import uuid
 from aws_dynamodb import AWSDynamoDB



client = AWSDynamoDB()
client.set_table_name("Test")
client.get_table_schema()
uuid = uuid.uuid1()
region = "#Chile"
extra_data = {
    "name": "Sebastian",
    "last_name": "Benavente",
    "age": 27,
    "married": False,
    "heigth": 1.71
}
data_send = {
    "uuid": str(uuid),
    "region": region,
    **extra_data

}
if client.table_exist:
    # Create or update element
    response = client.put_item(data_send)
    print(response)
 ```
 
 - Obtener elemento
 ``` python
client = AWSDynamoDB()
client.set_table_name("Test")
if client.table_exist:
    # get element
    primary_key = {
        "uuid": "uuid",
        "region": "region"
    }
    response = client.get_item(primary_key)
    print(response)

 ```
