import uuid
from aws_dynamodb import AWSDynamoDB

if __name__ == "__main__":

    client = AWSDynamoDB()
    client.set_table_name("Test")
    print(client.get_table_schema())
    
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
        """
        # Create or update element
        response = client.put_item(data_send)
        print(response)
        """
        # get element
        primary_key = {
            "uuid": "3d19e05e-2b66-11eb-b485-3ca067b2df49",
            "region": "#Chile"
        }
        response = client.get_item(primary_key)
        print(response)
    