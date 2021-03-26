import praw
import time
from configparser import ConfigParser

r = praw.Reddit('bot1')

#Collecting variables
while True:

    try:
        parser = ConfigParser()
        parser.read('config.cfg', encoding='utf-8')

        subreds = (parser.get("config", "subred"))
        subreds = list(subreds.split(","))

        keywords = (parser.get("config", "keywords"))
        keywords = list(keywords.split(","))

        break

    except:
        print("There was an error while getting data from config file. Correct any mistakes!")
        print("Trying again in 10 seconds.")
        time.sleep(10)

comment_body = ("""Oh! Seems you are talking about *this disease*. Here it the etimology for you:\n
**Myalgic Encephalomyelitis** (ME) = muscle pain with inflammation of the brain and spinal cord \n
**myalgic-**|**pain in one or more muscles**
-|-
**encephalo-**|brain
**myelitis**|inflammation of the spinal cord or of the bone marrow
**Fibromyalgia** (FM) = chronic pain, especially in the muscles \n
**fibro-**|**fibrous tissue**
-|-
**myalgia**|pain in one or more muscles
\n *Beep boop. I am a bot created by u/michaelangelito.*
""")

#Start running
print("Beep. Boop. Bot is booting...")
print("B0T by u/michaelangelito. Visit https//xval.me!")
print("--------------------")
time.sleep(1)

while True:
    for subred in subreds:
        subreddit = r.subreddit(subred)
        print("Getting posts in " + subred)

        for submission in subreddit.new(limit=1000):      #Gets the last submissions
            if checker(submission.title) == 2 or checker(submission.selftext) == 2:     #Detecting if already was saved
                if verify(submission) == 0:
                    print("Found a post with one of keywords.")
                    submission.reply(comment_body)

    print("Sleeping for 60seconds...")
    time.sleep(60)
       
def commenter(submission):
    submission.reply(comment_body)

def verify(submission):

    replies = submission.comments

    for x in replies:
        if x.author == "sxtybot":
            return 2
    else:
        return 0

def checker(text):
    text = list(text.split())

    for p in text:
        text.remove(p)
        p = p.replace(',',"")
        p = p.replace(';',"")
        p = p.replace(':',"")
        p = p.replace('!',"")
        p = p.replace('?',"")
        text.append(p)

    for keyword in keywords:
        for word in text:
            if word == keyword:
                return 2
    else:
        return 0
