import json
import requests
from django.db import connection
from rest_framework.views import exception_handler

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
#
# def user_securityPoint(userid):
#     mycursor = connection.cursor()
#     query = 'CALL sp_get_security_points(%s)'
#     mycursor.execute(query, (userid))
#     user_security_point = ","
#     for s_p_intuple in mycursor:
#         user_security_point += str(s_p_intuple[0]) + ","
#     return user_security_point
# def user_details(uid):
#     data = {}
#     mycursor = connection.cursor()
#     query = "call sp_user_details(%s)"
#     try:
#         mycursor.execute(query,[uid])
#         rows = mycursor.fetchone()
#         columns = [col[0] for col in mycursor.description]
#         for index, item in enumerate(rows):
#             data[columns[index]] = rows[index]
#         return data
#     except:
#         print('user_details not found')
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    print(response)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response