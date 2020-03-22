<h1> Python Gmail Rank Stacking </h1>
<hr>
Purpose: Provides a web interface using the gmail API to pull your emails and rank them based on your keyword criteria. The current use case is to pull emails from job recruiters and stack them based on keywords you define to save you time in identifying the job emails best suited to your interests or qualifications.
<hr>
<h2>Setup Requirements</h2>
<ul>
  <li>Clone or download rankstack.py and the templates folder/contents to your local machine/server</li>
  <li>Visit https://developers.google.com/gmail/api/quickstart/python and complete step 1 to enable the API. Save the credentials.json file in the same directory as pygmailapi.py</li>
  <li>install python3</li>
  <li>Install Pip3</li>
  <li>pip install required modules using: "pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib bs4 flask"</li>
  </ul>
  <h2>Tweaking your defined Query / Keywords</h2>
  <ul>
   <li>Edit your email search query in the following line within rankstack.py: (use https://support.google.com/mail/answer/7190?hl=en for search query guidance)</li>
  <li>results = service.users().messages().list(userId='me',labelIds = ['INBOX'], q='job opportunity OR position OR openings OR roles OR hiring newer_than:30d').execute()</li>
  <li>Edit your keyword rank criteria in the following line within rankstack.py:</li>
  <li>stackrank = ['CCNA', 'CCNP', 'LAN', 'Cisco','Network Engineer', 'Salary', 'Remote']</li>
  </ul>
  <h2>Running the Software:</h2>
  <ul>
   <li>Call pygmailapi.py with "python ./rankstack.py". You will be prompted to authenticate with Gmail on the first run</li>
  <li>Once running, you can navigate in your browser to: http://127.0.0.1:5000 to view the web interface.</li>
  </ul>
  
<h2>What the web interface looks like: (sensitive data blacked out)</h2>
<img src="http://www.blamethenetwork.com/wp-content/uploads/2020/03/Screen-Shot-2020-03-22-at-2.32.20-PM.png" />
You can sort based on any column, and search for keywords found in any field from the web interface.
