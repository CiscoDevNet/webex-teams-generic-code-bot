flows = {
    "add_init": {
        "message 1" : "Enter your initiative name. This will create a Webex Teams room with that name.",
        "message error 1" : "You already have an initiative of that name. Please enter a unique name.",
        "message end" : "Thank you! That room and file has been created for you!"
    },
    "add_codes" : {
        "message error 0" : "No existing initiatives. Message me 'add_init' to create an initiative before adding codes.",
        "message 1" : "To which initiative would you like to add codes? Enter the number next to the initiative.",
        "message error 1" : "That number is not listed above, please try again.",
        "message 2" : "Great! Now how many codes would you like generated (max 1000) and how long would you like them (max 10 chars) - seperate with comma",
        "message error 2" : "those are not valid entries, please try again.",
        "message end" : "Thanks! The codes have been generated and added initiative room specified."
    },
    "clear_codes" : {
        "message 1" : "From which initiative would you like to clear codes? Enter the number next to the initiative. Note: this will clear all codes and claimant information and cannot be undone. Proceed with caution.",
        "message error 1" : "That number is not listed above, please try again.",
        "message end" : "Thanks! The codes have been cleared from the initiative file you specified. See the files section of this room."
    },
    "clear_codes_assigned" : {
        "message 1" : "From which initiative would you like to clear assigned codes? Enter the number next to the initiative. Note: this will clear all codes and claimant information from already assigned codes and cannot be undone. Proceed with caution",
        "message error 1" : "That number is not listed above, please try again.",
        "message end" : "Thanks! The codes have been cleared from the initiative file you specified and new codes have been added to reset total number. See the files section of this room."
    },
    "clear_codes_unassigned" : {
        "message 1" : "From which initiative would you like to clear unassigned codes? Enter the number next to the initiative. Note: this will clear all unassigned codes and cannot be undone. Proceed with caution\n",
        "message error 1" : "That number is not listed above, please try again.",
        "message end" : "Thanks! The codes have been cleared from the initiative file you specified and new codes have been added to reset total number. See the files section of this room."
    },
    "delete_init" : {
        "message 1" : "Which initiative would you like to delete? Note: this will clear all initiative files and rooms and cannot be undone.",
        "message error 1" : "That number is not listed above, please try again.",
        "message end" : "Thanks! The codes have been cleared from the initiative file you specified and new codes have been added to reset total number. See the files section of this room."
    },
    "export_init" : {
        "message 1" : "Which initiative would you like to export?",
        "message error 1" : "That number is not listed above, please try again.",
        "message end" : "Thanks! Here is your .csv of that initiative."
    },
    "claim_code" : {
        "message 1" : "Hi There! I presume you've been given a code and told to message me. Please enter the code you were given.",
        "message error 1" : "That is not a valid code or it has already been claimed. Please try again.",
        "message end" : "Thanks!  You've been added to the appropriate room!"
    },
    "admin" : {
        "message 1" : "Hi there! I'm the Code Claim Bot and you're Admin! \n\n" \
                + "I can do the following \n\n" \
                + "* add_init - Create an initiative. This will create a new teams room that will track the codes created and claimed to that initiative\n" \
                + "* add_codes - Create up to 1000 pseudo random alpha-numeric codes (up to 10 characters) for an intitiative and save them in a .csv file here. If there are already codes for an intitiave they will be appended to the existing list of codes.\n" \
                + "* clear_codes - This will delete all codes, assigned or not  \n" \
                + "* clear_codes_assigned - This will delete all assigned codes and generate new codes in the same number \n" \
                + "* clear_codes_unaassigned - This will delete all unassigned codes and no new codes can be claimed \n" \
                + "* delete_init - This will delete an initiative, including codes and rooms\n" \
                + "* export_init - This will create an export of the claim codes and their claimants' first name, last name, and email address\n" 
    },
    "general_error" : {
        "message 1" : "I'm sorry I do not understand what you are saying. Please say response with 'claim_code' to claim your code"
    }
}
