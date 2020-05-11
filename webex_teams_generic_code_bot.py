"""This Webex teams bot does the following"""
from flows import flows
from flask import Flask, jsonify,abort,request,redirect
import requests
from webexteamssdk import WebexTeamsAPI
import sys, getopt
import json
from pprint import pprint
import csv
import random


# Configuration and parametes for WEBEX TEAMS
access_token="bot access token here"
teamsapi = WebexTeamsAPI(access_token=access_token)
botid = "bot id here"

bot_functions = Flask(__name__)

@bot_functions.route('/handler', methods=['POST'])
def message_handler():
    '''Receives message, parses room_id and person_id.  Called on POST to /handler.'''
    message_data = json.loads(request.data)
    room_id = message_data["data"]["roomId"]
    person_id = message_data["data"]["personId"]
    # Make sure bot doesn't respond to itself
    if person_id != botid:
        # Get the last x messages
        message_list = json.loads(get_messages(room_id))["items"]
        current_message = message_list[0]["text"]
        if len(message_list) > 1:
            previous_message = message_list[1]["text"]
        else:
            previous_message = ""
        current_flow = ""
        for message in message_list:
            if message["text"].find("claim_code") > -1 or message["text"].find("claim_code") > -1:
                current_flow = 'claim_code'
                break
            elif any(word in message["text"] for word in flows.keys()):
                current_flow = message["text"]
                break
        message_parser(room_id, current_message, previous_message, current_flow,person_id)
    
        
    return "message received"

def get_messages(room_id):
    headers = {"Authorization": f"Bearer {access_token}"}
    print(requests.get(url=f"https://api.ciscospark.com/v1/messages?roomId={room_id}&max=10", \
        headers=headers).text)
    return requests.get(url=f"https://api.ciscospark.com/v1/messages?roomId={room_id}&max=10", \
        headers=headers).text


def message_parser(room_id, current_message, previous_message, current_flow,admin_user):   
    if current_flow == 'claim_code':
        # This kicks off claim_code flow
        if current_message.lower().find("claim_code") > -1:
            claim_code(room_id, current_message, 1, admin_user)
        elif previous_message == flows["claim_code"]["message 1"] or previous_message == flows["claim_code"]["message error 1"]:
            claim_code(room_id, current_message, 2, admin_user)
    elif current_flow == 'admin':
        admin(room_id, 1)
    elif current_flow == 'add_init':
        if current_message.lower().find("add_init") > -1:
            add_init(room_id,1,current_message,admin_user)
        elif previous_message == flows["add_init"]["message 1"] or previous_message == flows["add_init"]["message error 1"]:
            add_init(room_id,2,current_message,admin_user)
    elif current_flow == 'add_codes':
        if current_message.lower().find("add_codes") > -1 or previous_message == flows["add_codes"]["message error 0"]:
            add_codes(room_id,1,current_message, previous_message)
        elif previous_message.find(flows["add_codes"]["message 1"]) > -1 or previous_message == flows["add_codes"]["message error 1"]:
            add_codes(room_id,2,current_message, previous_message)
        elif previous_message.find(flows["add_codes"]["message 2"]) > -1 or previous_message.find(flows["add_codes"]["message error 2"]) > -1:
            add_codes(room_id,3,current_message, previous_message)
    
    else:
        teamsapi.messages.create(room_id, markdown=flows["general_error"]["message 1"])

def claim_code(room_id, current_message,  step, person_id):
    if step == 1:
        teamsapi.messages.create(room_id, markdown=flows["claim_code"]["message 1"])
    elif step == 2:
        botrooms = teamsapi.rooms.list(type="group",sortby="created")
        tracker_room = ""
        initiative_room = ""
        team_id = ""

        for botroom in botrooms:
            if botroom.title.find("Claim Tracker") > -1:
                tracker_room = botroom.id
                messages = teamsapi.messages.list(botroom.id,mentionedPeople=botid)
                for message in messages:
                    message = message.text.split()
                    if "codes" in message:
                        codes = message[message.index("codes")+1]
                        codes = codes.split(",")
                        if current_message in codes:
                            for code_claim_message in messages:
                                code_claim_message = code_claim_message.text.split()
                                print(code_claim_message)
                                if current_message in code_claim_message and "codes" not in code_claim_message:
                                    print("already claimed")
                                    teamsapi.messages.create(room_id, markdown=flows["claim_code"]["message error 1"])
                                    return
                                elif "created:" in code_claim_message:
                                    print("not already claimed, breaking")
                                    initiative_room = code_claim_message[code_claim_message.index("created:") + 1]
                                    teamsapi.messages.create(room_id, markdown=flows["claim_code"]["message end"])
                                    claimant = teamsapi.people.get(person_id)
                                    teamsapi.messages.create(tracker_room, markdown=f"<@personId:{botid}> {current_message} claimed by {claimant.firstName} {claimant.lastName}, {claimant.emails}: {person_id}")
                                    teamsapi.memberships.create(initiative_room, person_id)
                                    if "teamId:" in code_claim_message:
                                        team_id = code_claim_message[code_claim_message.index("teamId:") + 1]
                                        teamsapi.team_memberships.create(team_id, personId=person_id)
                                    return
                print("not a valid code")
                teamsapi.messages.create(room_id, markdown=flows["claim_code"]["message error 1"])
                return

                                    

    
def admin(room_id, step):
    teamsapi.messages.create(room_id, markdown=flows["admin"]["message 1"])

def add_init(room_id, step, message, admin_user):
    if step == 1:
        teamsapi.messages.create(room_id, markdown=flows["add_init"]["message 1"])
    elif step == 2:
        botrooms = teamsapi.rooms.list(type="group",sortby="created")
        for botroom in botrooms:
            if botroom.title == message:
                teamsapi.messages.create(room_id, markdown=flows["add_init"]["message error 1"])
                return 
        
        # Create Tracker Room
        new_tracker_room = teamsapi.rooms.create(f"{message} Claim Tracker")
        teamsapi.memberships.create(new_tracker_room.id, personId=admin_user)
        teamsapi.messages.create(room_id, markdown=f"{message} Claim Tracker created: {new_tracker_room.id} ")

        # Create Initiative Room
        new_room = teamsapi.rooms.create(f"{message}")
        teamsapi.memberships.create(new_room.id, personId=admin_user)
        teamsapi.messages.create(room_id, markdown=f"{message} created: {new_room.id}")
        teamsapi.messages.create(new_tracker_room.id,  markdown=f"<@personId:{botid}> {message} created: {new_room.id}")
        """
        with open(message+'.csv', 'w', newline='') as csvfile:
            code_file = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            code_file.writerow([message, new_room.id])

        teamsapi.messages.create(room_id, files=[message+'.csv'])
        """

def add_codes(room_id, step, message, previous_message):
    existing_inits = ""
    existing_inits_dict = {}
    botrooms = teamsapi.rooms.list(type="group",sortby="created")
    if botrooms != None:
        index = 0
        for botroom in botrooms:
            if botroom.title.find("Claim Tracker") > -1:
                index += 1
                existing_inits += f"{index}. {botroom.title} \n"
                existing_inits_dict.update({str(index):botroom.id})
    else:
        teamsapi.messages.create(room_id, markdown=flows["add_codes"]["message error 0"])
        return

    if step == 1:
        teamsapi.messages.create(room_id, \
        markdown=f'{flows["add_codes"]["message 1"]} \n {existing_inits}')      
    elif step == 2:
        if message not in existing_inits_dict.keys():
            teamsapi.messages.create(room_id, markdown=flows["add_codes"]["message error 1"]) 
        else:
            teamsapi.messages.create(room_id, markdown=f'You have selected {message}.  {flows["add_codes"]["message 2"]}')
    elif step == 3:
        message = message.replace(" ", "")
        message = message.split(",")
        init_room_key = previous_message.split()[3].replace(".", "")
        init_room = existing_inits_dict[init_room_key]
        if len(message) == 2 and message[0].isnumeric and message[1].isnumeric:
            num_codes = int(message[0])
            num_chars = int(message[1])

            codes = generate_codes(num_codes, num_chars)
            teamsapi.messages.create(init_room, markdown=f"<@personId:{botid}> codes {','.join(codes)}")
            teamsapi.messages.create(room_id, markdown=flows["add_codes"]["message end"])
        else:
            teamsapi.messages.create(room_id, markdown=f'You had initiative {init_room_key}. However, {flows["add_codes"]["message error 2"]}')

def generate_codes(num_codes, num_chars):
    code_list = []
    
    for code in range(num_codes):
        individual_code = ""
        for code_part in range(num_chars):
            individual_code += "".join(
                random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(1)
            )
        code_list.append(individual_code)

    return code_list
        

      
        



if __name__ == "__main__":
    # Start the web server
    bot_functions.run(host='0.0.0.0', port=5006, threaded=True, debug=False)