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

comment_body = ("""Oh! Seems you are talking about the *Myalgic Encephalomyelitis ME/CFS*, which is muscle pain with inflammation 
of the brain and spinal cord. Let me explain the etimology for those who don´t know about it:\n

**myalgic-**|pain in one or more muscles
-|-
**encephalo-**|brain
**myelitis**|inflammation of the spinal cord or of the bone marrow
\n
*^(Beep boop. I am a bot created by u /michaelangelito. If I am being boring please contact my creator.)*
""") 

def main():
    try:
        for subred in subreds:
            subreddit = r.subreddit(subred)
            print("Getting posts in " + subred)

            y = 0

            for submission in subreddit.new(limit=1000):      #Gets the last submissions
                y = y + 1
                print(y)
                if checker(submission.title) == 2:     
                    if verify(submission) == 0:     #Detecting if already was saved

                        try:
                            print("Found a post with one of the keywords.")
                            submission.reply(comment_body)
                        except:
                            time.sleep(120)
                            submission.reply(comment_body)

                if checker_comments(submission) != 0:
                    if verify(submission) == 0:
                        print("Found a comment with one of the keywords.  - " + submission.title)
                        id = checker_comments(submission)

                        comment = r.comment(id=id)

                    try:
                        comment.reply(comment_body)
                    except:
                        time.sleep(120)
                        comment.reply(comment_body)

        print("Sleeping for 60seconds...")
        time.sleep(60)
        main()
    except Exception as e:
        print("Error")
        print(e)
        time.sleep(10)
        main()

def verify(submission):

    submission.comments.replace_more(limit=None)

    for comment in submission.comments.list():

        if comment.author == "me-cfs-fibro_Bot":
            return 2


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

def checker_comments(submission):
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():

        comment_text = comment.body
        id = comment.id
        text = list(comment_text.split())

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
                    return (id)
    
    return 0




#Start running
print("Beep. Boop. Bot is booting...")
print("B0T by u/michaelangelito. Visit https//xval.me!")
print("--------------------")
time.sleep(1)
main()
