import codecs
import tweepy
import time
import  sys
import csv
import json
from tweepy import OAuthHandler
import nltk
import re
import tkinter as tk
from tkinter import *
from tkinter.font import BOLD

violet =  "#262223"

pink = '#DDC6B6'

def createWidgets():

    
    #main Window
    root.frame1 = Frame(root, background= pink , bd=2,relief="flat")
    root.frame1.place(relx=0.5, rely=0.01, relwidth=0.96, relheight=0.1, anchor='n')
    #print Heading    
    root.text_title = Label(root.frame1,text="Sentimet Analysis For Hindi Tweets",bg=pink,fg=violet,font=('sans serif serif ', 20, BOLD )) 
    root.text_title.place(relx=0,relheight=0.95)


    #Second Frame
    root.frame2 = Frame(root, background=pink, bd=1,relief="flat")
    root.frame2.place(relx=0.5, rely=0.16, relheight=0.15, relwidth=0.96, anchor='n')
    # print on top
    root.labelf2 = Label(root.frame2, text='Enter Your Hindi Keyword', fg=violet, bg=pink, font=('sans serif ', 18 ))
    root.labelf2.place(relx=0.5, rely=0.01,relheight=0.5 , anchor='n')
    # Search groove
    root.saveLocationEntry = Entry(root.frame2 ,textvariable=keyWord,bd=7,relief="sunken",bg= violet,fg=pink,font=('sans serif ', 18, BOLD ))
    root.saveLocationEntry.place(relx=0.35,rely=0.55, relwidth=0.65, relheight=0.4,anchor='n')
    #search Button
    root.button0=Button(root.frame2,bd=7,bg=violet,fg=pink,text='Search',font=('sans srif',15,BOLD),command=search_start,relief="raised")
    root.button0.place(relx=0.85,rely=0.55,relwidth=0.275,relheight=0.4,anchor='n')



    #third frame
    root.frame3 = Frame(root, background=pink, bd=1,relief="flat")
    root.frame3.place(relx=0.5, rely=0.35, relheight=0.5, relwidth=0.96, anchor='n')
    #print Display Window
    root.lowerDisp = Label(root.frame3,text="Display Window" ,font=('sans serif', 18),relief="flat",fg=violet,bg=pink)
    root.lowerDisp.place(rely=0.02, relx=0.5, relwidth=0.96, relheight=0.1, anchor='n')
    #Output Window
    root.lowerDisp = Label(root.frame3, font=('sans serif', 15,BOLD),relief="solid",bg=violet,fg=pink)
    root.lowerDisp.place(rely=0.15, relx=0.5, relwidth=0.96, relheight=0.8, anchor='n')
    msg=f'Welcome\nDetails Will Be Dispayed Here\n\nStarting Authentication..!!\n\nAuthentication Done..!!\nLogged In Successfully\n\nClick On Train First'
    root.lowerDisp.config(text=msg)

    
    #fourth frame
    root.frame4 = Frame(root, background=pink, bd=1,relief="flat")
    root.frame4.place(relx=0.5, rely=0.88, relheight=0.1, relwidth=0.96, anchor='n')

    root.button1=Button(root.frame4,bd=7,bg=violet,fg=pink,text='Train',font=('sans srif',15,BOLD),command=start_train,relief="raised")
    root.button1.place(relx=0.25,rely=0.1,relwidth=0.45,relheight=0.8,anchor='n')

    root.button2=Button(root.frame4,bd=7,bg=violet,fg=pink,text='Quit',font=('sans srif',15,BOLD),command=quitApplication,relief="raised")
    root.button2.place(relx=0.75,rely=0.1,relwidth=0.45,relheight=0.8,anchor='n')
    
    


    
def search_start():
    

    access_token = "103589925-PYiNRi6sAoSAFCau7Q5zDAqF7Kt8WwsK5EunWL3I"
    access_token_secret = "u8N1nS93eN5npmtBOAxCwJgZE0W4wPCNe1CEuCB9lEIys"
    consumer_key = "IIFBxSZv8YnhRJuvvDJVkR4ht"
    consumer_secret = "zou3XOVMDXp9esingDNEowUeEPmTKkY4daZGYdmalovyd9JCxr"


    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                   wait_on_rate_limit_notify=True)
    if api:
        pass
    if (not api):
        msg="Can't Authenticate"
        root.lowerDisp.config(text=msg)
        sys.exit(-1)
        
    keyword=keyWord.get()

    msg1=f"Fetching {keyword}...\nScanning Twitter For Latest\nTweets Related To {keyword}\n\nPlease Wait Whhile Results are Evaluated "
    messagebox.showinfo("Search Started",msg1)
    root.lowerDisp.config(text=msg1)

    tweetCount=0
    maxTweets=100
    neg=0
    pos=0
    cnt=0
    while tweetCount < maxTweets:
        try:
            #crawling in hindi and hence the option of 'hi'
            newTweets=api.search(q=keyword, lang="hi", count=100)
            for tweet in newTweets:
                # printing only tweet
                #print (tweet.text)
                #print (":"*80)
                Tweet = tweet.text
                Tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',Tweet)
                Tweet = re.sub('@[^\s]+','TWITTER_USER',Tweet)
                Tweet = re.sub('[\s]+', ' ', Tweet)
                Tweet = re.sub(r'#([^\s]+)', r'\1', Tweet)
                Tweet = Tweet.strip('\'"')
                a = ':)'
                b = ':('
                Tweet = Tweet.replace(a,'')
                Tweet = Tweet.replace(b,'')
                tag = 'TWITTER_USER' 
                rt = 'RT'
                url = 'URL'
                Tweet = Tweet.replace(tag,'')
                tweetCount+=1
                if rt in Tweet:
                    continue
                Tweet = Tweet.replace(url,'')
               
                res = classifier.fn1(Tweet)
                #print ("\n",res)
                if res == "negative":
                    neg=neg+1
                    #print("Negative = ",neg)
                elif res == "positive":
                    pos=pos+1
                    #print("positive= ", pos)
                cnt=cnt+1
                    
        except tweepy.TweepError as e:
            #print("some error : " + str(e))
            msg=f"some error : {str(e)} "  
            root.lowerDisp.config(text=msg)
            
            #print("retrying in 20 seconds")
            msg="retrying in 20 seconds"
            root.lowerDisp.config(text=msg)
            time.sleep(20)
            
    per1=((float(pos)/cnt)*100)
    per2=((float(neg)/cnt)*100)
    #print(f"Positive Tweets Are {per1} %")
    #print(f"Negative Tweets Are {per2} %")
    #print("Thank You For Using This Application :) ")
    msg=f"Results :\n\nPositive Tweets Are {per1} %\n\nNegative Tweets Are {per2}\n\nTotal Tweets Reffered : 1000 "
    root.lowerDisp.config(text=msg)


def start_train():
    messagebox.showinfo("Training Started","Traing Of Available Data Started..!\nPlease Wait This Might Take a While..\n\nPlease Wait for 2 Minutes")                
    global classifier
    import classifier
    
    msg=f"Training Completed..!!\n\nYou Can Now Search For Keywords"
    root.lowerDisp.config(text=msg)
    

def quitApplication():
    messagebox.showinfo("Exit Application","Thank You For Using This Application...!!!\n\nRegards : Kanishka Patel")
    root.destroy()



root = tk.Tk()

root.title("Mini Project ...!!!")
root.geometry("800x700")
root.resizable(False, False)
root.configure(background = violet)
keyWord = StringVar()


createWidgets()

root.mainloop()
