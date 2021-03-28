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

comment_body = ("""Oh! Seems you are talking about the *Myalgic Encephalomyelitis ME/CFS*, which is muscle pain with inflammation of the brain and spinal cord.
Let me explain the etimology for those who don´t know about it:\n
**Myalgic Encephalomyelitis** (ME) = muscle pain with inflammation of the brain and spinal cord \n
**myalgic-**|**pain in one or more muscles**
**encephalo-**|brain
**myelitis**|inflammation of the spinal cord or of the bone marrow
**Fibromyalgia** (FM) = chronic pain, especially in the muscles \n
**fibro-**|**fibrous tissue**
**myalgia**|pain in one or more muscles
\n 
ME is also known as Chronic Fatigue Syndrome (CFS/ME):
\n
>People with ME/CFS are often not able to do their usual activities. At times, ME/CFS may confine them to bed. 
People with ME/CFS have overwhelming fatigue that is not improved by rest. ME/CFS may get worse after any activity, whether it’s physical or mental. 
This symptom is known as post-exertional malaise (PEM). Other symptoms can include problems with sleep, thinking and concentrating, pain, 
and dizziness. People with ME/CFS may not look ill.
\n
FM has been called the invisible disease with so many different names.
\n
>Fibromyalgia (fi·bro·my·al·gi·a) is a condition that causes pain all over the body (also referred to as widespread pain), sleep problems, fatigue, 
and often emotional and mental distress. People with fibromyalgia may be more sensitive to pain than people without fibromyalgia. This is called 
abnormal pain perception processing. Fibromyalgia affects about 4 million US adults, about 2% of the adult population. 
The cause of fibromyalgia is not known, but it can be effectively treated and managed.

\n
Source: https://cdc.gov  \n*^(Beep boop. I am a bot created by u /michaelangelito ^(Check ^https://xval.me ^for ^more ^stuff). 
^(If ^I ^am ^being ^boring ^please ^contact ^my ^creator.)*
""") 

def main():
    try:
        for subred in subreds:
            subreddit = r.subreddit(subred)
            print("Getting posts in " + subred)

            for submission in subreddit.new(limit=1000):      #Gets the last submissions
                if checker(submission.title) == 2 or checker(submission.selftext) == 2:     #Detecting if already was saved
                    if verify(submission) == 0:
                        try:
                            print("Found a post with one of keywords.")
                            submission.reply(comment_body)
                        except:
                            time.sleep(120)

        print("Sleeping for 60seconds...")
        time.sleep(60)
        main()
    except Exception as e:
        print("Error")
        print(e)
        time.sleep(10)
        main()

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


#Start running
print("Beep. Boop. Bot is booting...")
print("B0T by u/michaelangelito. Visit https//xval.me!")
print("--------------------")
time.sleep(1)
main()
