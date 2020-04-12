import json
import requests
from django.db import connection

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

# def user_securityPoint(userid):
#     mycursor = connection.cursor()
#     query = 'CALL sp_get_security_points(%s)'
#     mycursor.execute(query, (userid))
#     user_security_point = ","
#     for s_p_intuple in mycursor:
#         user_security_point += str(s_p_intuple[0]) + ","
#     return user_security_point
