## get Box.com developer API key: https://uofi.app.box.com/developers/console/app/416846/configuration
##  save the above to last line of app.cfg; note it has to be changed every hour due to the box.com license
## experts swagger examples: https://experts.illinois.edu/ws/api/59/api-docs/index.html

######
## Variables _you_ need to supply
######
YOUR_FILE_ID =  # file id of box.com csv list of faculty
YOUR_API_KEY =  # your api key to use uillinois Experts

# Import two classes from the boxsdk module - Client and OAuth2
from boxsdk import Client, OAuth2
import re
import html2text

# Define client ID, client secret, and developer token.
CLIENT_ID = None
CLIENT_SECRET = None
ACCESS_TOKEN = None

# Read app info from text file
with open('app.cfg', 'r') as app_cfg:
    CLIENT_ID = app_cfg.readline()
    CLIENT_SECRET = app_cfg.readline()
    ACCESS_TOKEN = app_cfg.readline()

# print ("CLIENT_ID:%s" % CLIENT_ID)
# print ("CLIENT_SECRET:%s" % CLIENT_SECRET)
# print ("ACCESS_TOKEN:%s" % ACCESS_TOKEN)

# Create OAuth2 object. It's already authenticated, thanks to the developer token.
oauth2 = OAuth2(CLIENT_ID, CLIENT_SECRET, access_token=ACCESS_TOKEN)

# Create the authenticated client
client = Client(oauth2)

# file_id: csv formatted list of faculty names (columns 1,2), email (col 3) and netid (4)
my_file_id=YOUR_FILE_ID

import html2text

lines = client.file(file_id=my_file_id).content().decode("utf-8", "replace").splitlines()

import requests
import json
import numpy

baseURL = "https://experts.illinois.edu/ws/api/59/persons/"
endpoint = "research-outputs.json"
apiKey = YOUR_API_KEY

f1=open('author_pubs.json','w')
f2=open('author_pubs.csv','w')

category="Microbes"

for line in lines[1:]:
    print (line)
    if line.count(',') == 2:
        print ('2:'+line)
        ## not sure why split(',',4) does not limit to 4 - I get an error when there are 5
        [lname, fname, email] = line.split(',')
        if '@' in email:
            # print ("id:" + str(id) + " category:" + str(category))
            print ("email:" + str(email) + " category:" + str(category))


            ## As of this writing, there is no flag to "get all" records from Elsevier, so the first request is to find out how many records match for this ID
            ## Worse, by default, the api requests do not pull all records, but rather a window of about 10 or so
            personId = email
            requestUrl = baseURL + personId + "/" + endpoint
            field1 = "count"
            navigationLink = "false"
            size = 1
            payload = (('apiKey',apiKey),('fields',field1),('navigationLink',navigationLink),('size',size))
        
            resp = requests.get(requestUrl, params=payload)
            print(resp.url)
            if resp.status_code != 200:
                # This means something went wrong.
                if resp.status_code == 404:
                    print("{'email': '" + str(personId) + "', 'status': 'Record not found'}")
                    f1.write("{'email': '" + str(personId) + "', 'status': 'Record not found'}\n")
                    outputStr = '** ' + fname + ',' + lname + ',' + personId + ',,RECORD NOT FOUND\n'
                    print(outputStr)
                    f2.write(outputStr)
                    continue

                else:
                    print ('Error with personID:' + str(personId))
                    raise ApiError('GET /tasks/ {}'.format(resp.status_code))

            ## Unfortunately, this can produce XML+Java errors, so I have to strip those out of the output
            m = re.search('..xml.+', resp.text, re.S)
            count = 0
            # print(m)
            if m:
                jsonText = resp.text[:m.start(0)]
                ## fix another bug (how many are there?)
                jsonText = re.sub(' : "\d+"','',jsonText)
                jsonText = re.sub('(, *{\s+})+','',jsonText, re.MULTILINE)
                myCountsJson = json.loads(jsonText)
                count = myCountsJson['count']
            else:
                count = resp.json()['count']

            print("Count: " + str(count))
        
            ##  After getting the count, I pass it as a "size" parameter to get all the relevant documents

            field1 = ""
            navigationLink = "false"
            size = count
            rendering = "apa"
            dateRange = "publicationDate.fromDate=2000&publicationDate.toDate=2010-10-12"
            fromDate = 2012
            ## tried to use publicatDate.fromDate, but it did not work
            payload = (('apiKey',apiKey),('rendering',rendering),('navigationLink',navigationLink),('size',size))

            resp = requests.get(requestUrl, params=payload)
            print(resp.url)
            if resp.status_code != 200:
                # This means something went wrong.
                outputStr = 'ERROR for ' + fname + ',' + lname + ',' + personId + '\n'
                print(outputStr)
                f2.write(outputStr)
                raise ApiError('GET /tasks/ {}'.format(resp.status_code))

            # print(resp.text)

            ## Unfortunately, this produces XML+Java errors, so I have to strip those out of the output
            m = re.search('..xml.+', resp.text, re.S)
            # print(m)
            if m:
                jsonText = resp.text[:m.start(0)]
            else:
                jsonText = resp.text

            ## fix another bug (how many are there?)
            jsonText = re.sub(' : "\d+"','',jsonText)
            jsonText = re.sub('(, *{\s+})+','',jsonText, re.MULTILINE)

            ## convert html to plain text
            ## jsonPlainText = html2text.html2text(jsonText)

            # print(jsonText)
        
            ## And finally I can load the results into a dictionary
            outputsJson = json.loads(jsonText)
            # print(outputsJson['items'][0])

            # f1.write(str(outputsJson))
            # f1.write("\n")

            for item in outputsJson['items']:

                itemDict = dict(item)
                render = itemDict.get('rendering')[0]
                renderDict = dict(render)
                # print(itemDict)
                # print(render)
                # print(renderDict)
                valueHTML = renderDict.get('value')
                multiLineValue = html2text.html2text(valueHTML)
                value = re.sub('\s*\n\s*', ' ', multiLineValue)
                value = re.sub('"','\'', value)
                ## strip out high-order utf8 characters
                cleanedValue = re.sub(r'[^\x00-\x7F]+',' ', value)
                # outputStr = personId + ',' + category + ',"' + cleanedValue + '"\n'
                
                m = re.search('\((\d{4})\)', cleanedValue)
                if m:
                    year = m.group(1)
                    print ("year: " + year)
                    if int(year)>(fromDate-1):
                        outputStr = fname + ',' + lname + ',' + personId + ',' + year + ',"' + cleanedValue + '"\n'
                        print(outputStr)
                        f2.write(outputStr)


    ## end of loop


f2.close()
f1.close()
