import logging

import boto3

from admin import (
    DB_ACCESS_KEY,
    DB_SECRET_KEY,
    DB_REGION_NAME,
)

logger = logging.getLogger()

def keywords(key):
    """Convert an attribute name to a shorthand name.
       This prevents such keys from conflicts with a DynamoDB reserved word
    """
    mapping = {
        'status': 's',
        'username': 'u',
        'bike_name': 'bn',
        'first_name': 'fn',
        'last_name': 'ln',
        'log': 'l',
        'type': 't',
    }
    return mapping.get(key, key)


def generate_expr(dict_, ignore=''):
    """Generate expressions required by boto for updating a table"""
    expr_attr_names = {}
    expr_attr_vals = {}
    update_expr_list = []

    for k, v in dict_.items():
        if k == ignore:
            continue

        expr_attr_vals[f':{keywords(k)}'] = v
        expr_attr_names[f'#{keywords(k)}'] = k
        update_expr_list.append(f'#{keywords(k)}=:{keywords(k)}')

    update_expr = 'set ' + ', '.join(update_expr_list)
    return update_expr, expr_attr_names, expr_attr_vals


def get_dynamodb():
    """Create a resource object."""
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=DB_ACCESS_KEY,
        aws_secret_access_key=DB_SECRET_KEY,
        region_name=DB_REGION_NAME)
    return dynamodb

def get_user_data(chat_id):
    """Getting user data as a dictionary"""
    table = get_dynamodb().Table('users')
    dict_ = table.get_item(Key={'chat_id': chat_id})

    try:
        return dict_['Item']
    except KeyError:
        return None

def set_user_data(chat_id, user_data):
    """Updating single user's data"""
    table = get_dynamodb().Table('users')

    update_expr, expr_attr_names, expr_attr_vals = generate_expr(user_data, ignore='chat_id')
    response = table.update_item(
        Key={
            'chat_id': chat_id,
        },
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_attr_vals,
        ExpressionAttributeNames=expr_attr_names,
        ReturnValues="UPDATED_NEW")

    return response

def get_bike_data(bike_name):
    """Getting bikes data as a dictionary"""
    table = get_dynamodb().Table('bikes')

    dict_ = table.get_item(Key={'name': bike_name})
    try:
        return dict_['Item']
    except KeyError:
        return None

def get_all_bikes():
    """Getting all bikes data to show"""
    table = get_dynamodb().Table('bikes')

    response = table.scan()
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    return data

def set_bike_data(bike_name, bike_data):
    """Updating single bike's data"""
    table = get_dynamodb().Table('bikes')

    update_expr, expr_attr_names, expr_attr_vals = generate_expr(bike_data, 'name')
    response = table.update_item(
        Key={
            'name': bike_name,
        },
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_attr_vals,
        ExpressionAttributeNames=expr_attr_names,
        ReturnValues="UPDATED_NEW"
    )

    return response

def get_username(username):
    """Getting username to chat_id mapping"""
    table = get_dynamodb().Table('usernames')
    dict_ = table.get_item(Key={'username': username})

    try:
        response = dict_['Item']
    except KeyError:
        return None

    return int(response['chat_id'])

def set_username(username, chat_id):
    """Updating username to chat_id mapping"""
    table = get_dynamodb().Table('usernames')

    response = table.update_item(
        Key={
            'username': username,
        },
        UpdateExpression='set chat_id=:chat_id',
        ExpressionAttributeValues={':chat_id': chat_id},
        ReturnValues="UPDATED_NEW")

    return response


if __name__ == '__main__':
    pass
