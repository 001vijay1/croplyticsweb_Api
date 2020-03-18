import json


def send_response(result, errorcode, errormessage, statuscode):
    body = {
        'ErrorCode': errorcode,
        'ErrorMessage': errormessage,
        'Result': result
    }
    # response = {
    #     'statusCode': statuscode,
    #     'body':json.dumps(body, default=str)
    # }
    return body


