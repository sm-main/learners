# yomamabot/fb_yomamabot/views.py
import json, requests, random, re
from pprint import pprint
from googleapiclient.discovery import build
from django.views import generic
from django.http.response import HttpResponse
from django.core.mail import send_mail

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#  ------------------------ Fill this with your page access token! -------------------------------
PAGE_ACCESS_TOKEN = "EAAQ9ItZASPjIBAGQIH8RxRpeHqvRLvscI9LTjTOrS4cS8tREOErZBB4l9F3efvUF1Yzi90u66ciDrenZBYJ3LaEKmiXnDeGDW1ibMDTBJ1iPCZAuWgu80ZCWytkWAKNWh8UKiK3En65LpOtYak3oomwp0fNi3kZA5T3FZAh94IgcwZDZD"
VERIFY_TOKEN = "2318934571"


my_api_key = "AIzaSyBF_TsL1lsW2R-rMMfLj_Iqw2_UVowKX1A"
my_cse_id = "011451716192923071187:sqtrnpnxrgm"
jokes = { 'hello': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                     """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
         'hi':      ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                      """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
         'hey there': ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
                  """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""]
              }


class LearnerBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '2318934571':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    # pprint(message)
                    
                    message_text_length = len(message['message']['text'].split(' '))
                    if message_text_length > 1:
                        post_facebook_message_google_search(message['sender']['id'], message['message']['text'])
                    else:
                        post_facebook_message(message['sender']['id'], message['message']['text'])
        return HttpResponse()

post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAChJAsIz2MBANMirDCA9IolztpMDSexUrXVIvhyWEopfnR9bbU8yaznQ2eRMqEHiH9ywNUdY1Nc6ZAYCKRfnUHh8TqhJWK52J1J8bZBH0QMGhrXFdaMFIqagdup7fUUo05bJe7wM9HLwejtoKK5dQQztwzj3v3aBZBpkRfvwZDZD'

def post_facebook_message_google_search(fbid, recevied_message):
    # response_msg =
    user_name_and_pic = 'Wait Fetching results from google..'
    service = build("customsearch", "v1",
                   developerKey=my_api_key)

    res = service.cse().list(
        q=recevied_message,
        cx=my_cse_id,
        searchType='text',
        num=3,
        # imgType='clipart',
        # fileType='png',
        safe= 'off'
    ).execute()

    if not 'items' in res:
        print('No result !!\nres is: {}'.format(res))
    else:
        for item in res['items']:
            print('{}:\n\t{}'.format(item['title'], item['link']))
            user_name_and_pic = item['title']
    response_msg = json.dumps({
                "recipient":{"id":fbid},
                "message":{"text": user_name_and_pic },
                            # "sender_action":"typing_on"
            })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)



def post_facebook_message(fbid, recevied_message):

    if recevied_message:
        # user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
        # user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':'EAAChJAsIz2MBANMirDCA9IolztpMDSexUrXVIvhyWEopfnR9bbU8yaznQ2eRMqEHiH9ywNUdY1Nc6ZAYCKRfnUHh8TqhJWK52J1J8bZBH0QMGhrXFdaMFIqagdup7fUUo05bJe7wM9HLwejtoKK5dQQztwzj3v3aBZBpkRfvwZDZD'}
        # user_details = requests.get(user_details_url, user_details_params).json()
        # print(user_details)
        user_name_and_pic = ' Welcome to Magicbricks messenger AI powered bot. Here to help you out with any real estate problem you are or may face. Search like : eg: "Houses in gurgaon", "east facing houses in delhi"'
        response_msg = json.dumps({
                    "recipient":{"id":fbid},
                    "message":{"text": user_name_and_pic },
                                # "sender_action":"typing_on"
                })
    # main(recevied_message)
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
        # pprint(status.json())





# from googleapiclient.discovery import build



#
# def main(q):
#   # Build a service object for interacting with the API. Visit
#   # the Google APIs Console <http://code.google.com/apis/console>
#   # to get an API key for your own application.
#   service = build("customsearch", "v1", developerKey=my_api_key)
#
#   res = service.cse().list(
#       q=q,
#       cx=my_cse_id,
#     ).execute()
#   print(res)
#
# if __name__ == '__main__':
#   main()
