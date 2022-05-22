from database.controller import get_dynamodb

def create_users_table():
    """Creates users table if it doesn't exist"""
    dynamodb = get_dynamodb()

    table = dynamodb.create_table(
        TableName='users',
        AttributeDefinitions=[
            {
                'AttributeName': 'chat_id',
                'AttributeType': 'N'
            },
        ],
        KeySchema=[
            {
                'AttributeName': 'chat_id',
                'KeyType': 'HASH'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    return table

def create_bikes_table():
    """Creates bikes table if it doesn't exist"""
    dynamodb = get_dynamodb()

    table = dynamodb.create_table(
        TableName='bikes',
        AttributeDefinitions=[
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            },
        ],
        KeySchema=[
            {
                'AttributeName': 'name',
                'KeyType': 'HASH'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    return table

def create_usernames_table():
    """Creates usernames table if it doesn't exist"""
    dynamodb = get_dynamodb()

    table = dynamodb.create_table(
        TableName='usernames',
        AttributeDefinitions=[
            {
                'AttributeName': 'username',
                'AttributeType': 'S'
            },
        ],
        KeySchema=[
            {
                'AttributeName': 'username',
                'KeyType': 'HASH'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    return table
