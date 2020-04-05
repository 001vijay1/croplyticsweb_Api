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


def SendSms(phoneNumber, message,messageType,projectId):
    url = 'https://90yw2sv2vk.execute-api.us-east-1.amazonaws.com/prod/message/SendSmsApi'
    try:
        data = {
            'accessKey':'ofwR5aLecQiAQAsqWu0LxwgUNWJ6fWUx',
            'secretKey':'ES9d7d7yeV',
            'phoneNumber':phoneNumber,
            'message':message,
            'messageType':messageType,
            'projectId':projectId
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        res = requests.post(url, data=json.dumps(data), headers=headers)
        # inserted = db.smslogs.insert_one({
        #                 'userId':userId,
        #                 'phonenumber':phoneNumber,
        #                 'message':message,
        #                 'eventTime': datetime.datetime.utcnow()
        #             })
    except Exception as e:
        print(e)
        res='Error'
    return res


# def user_securityPoint(userid):
#     mycursor = connection.cursor()
#     query = 'CALL sp_get_security_points(%s)'
#     mycursor.execute(query, (userid))
#     user_security_point = ","
#     for s_p_intuple in mycursor:
#         user_security_point += str(s_p_intuple[0]) + ","
#     return user_security_point
