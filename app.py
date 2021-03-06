from flask import Flask, request, redirect
import twilio.twiml
import random
import json
 
app = Flask(__name__)

#Key: Session Phone number, Value: Dreamboys number
session = {} 

with open('Dream_Boys.json') as data_file:    
    people = json.load(data_file) 

phone = {
    "+19732644177": "Joe",
    "+19733060490": "Eric",
    "+19735247011": "Rich",
    "+19733308109": "Lars",
    "+17323477185": "Tobias",
    "+17323477216": "Eddie",
    "+17322035203": "Shahan",
    "+17322109837": "Swift",
    "+16097265347": "Sam",
    "+16092514356": "Nick",
    "+16097265313": "Josh",
    "+16093035331": "Biggie",
}

categories = {
    'location': ['bar', 'cave', 'commune'],
    'food': ['pizza', 'nachos', 'wings', 'dumplings'],
    'travel': ['skateboard', 'bus', 'car', 'bike'],
    'language': ['ruby', 'python', 'javascript', 'go'],
}

base_url = "https://raw.githubusercontent.com/nickgirardo/dreamphone/master/assets/audio/final/"

@app.route("/", methods=['GET', 'POST'])
def voice_incoming():
    """Respond to incoming requests."""
    target = request.values.get('To', None)
    caller = request.values.get('From', None)
    
    resp = twilio.twiml.Response()

    if caller not in session:
        session[caller] = random.choice(phone.keys())
        print 'Dreamboy:' + session[caller]
        resp.say("Welcome to Dreamphone! Find your dream boy!")

    resp.gather(numDigits=1, action='/guess', timeout=5)

    target_profile = people[phone[target]]
    dream_profile = people[phone[session[caller]]]

    if target_profile['saysSpecial'] == phone[session[caller]]:
	roll = random.randint(0,9)
	if roll == 0:
		resp.play(get_special(phone[target], target_profile['saysSpecial']))
		return str(resp)

    category = target_profile['set']
    options = [x for x in categories[category] if x != dream_profile[category]]
    choice = random.choice(options)

    resp.play(get_clue(choice, phone[target]))
 
    return str(resp)

@app.route("/guess", methods=['GET', 'POST'])
def guess():
    """Respond to guess for dream boy"""
    target = request.values.get('To', None)
    caller = request.values.get('From', None)

    #Check if target is the dream boy here
    resp = twilio.twiml.Response()

    if caller not in session:
        #NO ACTIVE SESSION HANDLE THIS
        print 'invalid call to guess'
    elif session[caller] == target:
        resp.play(get_correct(phone[target]))
        del session[caller]
    else:
        resp.play(get_wrong(phone[target]))

    return str(resp)

def get_clue(choice, person):
    url = base_url  + str(person).lower() + "/no_" + str(choice) + ".wav"
    print url
    return url 

def get_correct(person):
    url = base_url + str(person).lower() + "/correct.wav"
    print url
    return url

def get_wrong(person):
    url = base_url + str(person).lower() + "/wrong.wav"
    print url
    return url

def get_special(target, dreamboy):
	url = base_url + str(target).lower() + "/" + dreamboy.lower() + "_special.wav"
	print url
	return url

if __name__ == "__main__":
    app.run(debug=True, port=3000)
