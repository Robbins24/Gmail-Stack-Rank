from __future__ import print_function
import pickle
import os.path
import base64
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import dateutil.parser as parser
import os
from flask import Flask, render_template


app = Flask(__name__)
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def getMail():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me',labelIds = ['INBOX'], q='job opportunity OR position OR openings OR roles OR hiring newer_than:30d').execute()
    messages = results.get('messages', [])
    emailsList = []

    if not messages:
        print ("No messages found.")
    else:
        for message in messages:
            stackrank = ['CCNA', 'CCNP', 'LAN', 'Cisco','Network Engineer', 'Salary', 'Remote']
            weight = 0
            temp_dict = {}
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            payload = msg['payload']
            header = payload['headers']
            if "data" in payload['body']:
                data = payload['body']
                body = list(data.values())[0]
            elif "data" in payload['parts'][0]['body']:
                body = payload['parts'][0]['body']['data']
            else:
                if "parts" in payload['parts'][0]:
                        if len(payload['parts'][0]['parts']) >= 3:
                            if "data" in payload['parts'][0]['parts'][2]['body']:
                                print("DATA FOUND IN PAYLOAD PARTS 0 PARTS 2 BODY****")
                                body = payload['parts'][0]['parts'][2]['body']['data']
                            else:
                                pass
                        else: 
                            body = "none"
                else:
                        body = "none"


                # PULLING IN HEADER INFO (Date, Sender, Subject)
            for one in header: # getting the Subject
                if one['name'] == 'Subject':
                    msg_subject = one['value']
                    temp_dict['Subject'] = msg_subject
                else:
                    pass


            for two in header: # getting the date
                if two['name'] == 'Date':
                    msg_date = two['value']
                    date_parse = (parser.parse(msg_date))
                    m_date = (date_parse.date())
                    temp_dict['Date'] = str(m_date)
                else:
                    pass

            for three in header: # getting the Sender
                if three['name'] == 'From':
                    msg_from = three['value']
                    temp_dict['Sender'] = msg_from
                else:
                    pass

            temp_dict['Snippet'] = msg['snippet'] # fetching message snippet


            # Cleaning up the Email Body
            if(body == "none"):
                print("NO EMAIL MESSAGE DATA FOUND")
            else:
                decode = base64.urlsafe_b64decode(body.encode("ascii")) # Decode the base64 data returned from the API for the body
                clean = BeautifulSoup(decode,"html.parser") # Strip out all of the html elements to get text only
                bodyclean = clean.get_text() # Email Body Data in Decoded/HTML Cleaned Format
            # Return the Results
            found = []
            for word in stackrank:
                if word in bodyclean:
                        weight += 25
                        found.append(word)
            email = {
            "Date" : temp_dict['Date'],
            "From" : temp_dict['Sender'],
            "Subject" : temp_dict['Subject'],
            "Excerpt" : temp_dict['Snippet'],
            "Weight" : weight,
            "Found" : ', '.join(found)
            }
            emailsList.append(email)

    rankstacked = sorted(emailsList, key=lambda k: k['Weight'], reverse=True)
    return rankstacked

        
@app.route("/")
def hello():
        rackstanked = getMail()
        return render_template('emails.html', rackstanked=rackstanked)


if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000, debug=True)
