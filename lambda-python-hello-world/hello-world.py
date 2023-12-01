def lambda_handler(event, context):
    message = 'Hello {}!'.format(event['name'])  
    return { 
        'message' : message
    }