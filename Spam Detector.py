# -*- coding: utf-8 -*-
"""
Spam Detector
Created by: Salomón Olivera
"""
import csv
from tkinter import *
from tkinter import messagebox

def check_if_is_in_dict(word,label):
    if word in mainDict[label]:
        mainDict[label][word] = mainDict[label][word] + 1
    else:
        mainDict[label][word] = 1
        
def add_words_to_dict(message,label):
    messageList = message.split( )
    for word in messageList:
        if word not in stopWords:
            if(word[-1:] == "." or word[-1:] == "," or word[-1:] == "!" or word[-1:] == "?"):
                check_if_is_in_dict(word[:-1].lower(),label)
            else:
                check_if_is_in_dict(word.lower(),label)

def probability_per_word(word,label):
    #Size of vocabulary
    vocabulary = len(mainDict['ham'].keys()) + len(mainDict['spam'].keys()) 
    if word in mainDict[label]:
        #How many times does that word appears in all the data set with that label
        occurrences = mainDict[label][word] + k
        #Normalize with the total words per label(no mather if it's repeated) plus the vocabulary 
        normalizedTotalLabel = totalWords[label] + vocabulary
        
        prob = occurrences / normalizedTotalLabel
    else:
        occurrences = 0 + k
        normalizedTotalLabel = totalWords[label] + vocabulary
        
        prob = occurrences / normalizedTotalLabel
    
    return prob

def validate_text(text_input):
    file = 'spam.csv'

    mainDict = {}
    mainDict['ham'] = {}
    mainDict['spam'] = {}
    spamCounter = 0
    hamCounter = 0
    stopWords = ['a','to','an','the','and']
    
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            label = row['Label']
            message = row['Message']
            if(label == 'ham'):
                hamCounter += 1
            else:
                spamCounter +=1
            
            add_words_to_dict(message,label)

    #Count total of words per label, no matter that the word is repeated
    countHamWords = 0
    for key in mainDict['ham'].keys():
        countHamWords = countHamWords + mainDict['ham'][key]
    
    countSpamWords = 0
    for key in mainDict['spam'].keys():
        countSpamWords = countSpamWords + mainDict['spam'][key]
    
    totalWords = {}
    totalWords['ham'] = countHamWords
    totalWords['spam'] = countSpamWords
    
    k = 1
    totalMessages = spamCounter + hamCounter
    
    #Laplace smoothing
    dividePrior = totalMessages + (2 * k)
    #Number of messages labeled plus k
    priorSpam = (spamCounter + k) / dividePrior
    priorHam = (hamCounter + k) / dividePrior
    
    probBeingSpam = priorSpam
    probBeingHam = priorHam
    

    messageList = text_input.split( )
    
    #Iterate through all the words in the message and calculate the probability per word
    for word in messageList:
        if word not in stopWords:
            if(word[-1:] == "." or word[-1:] == "," or word[-1:] == "!" or word[-1:] == "?"):
                wSpam = probability_per_word(word[:-1].lower(),'spam')
                wHam = probability_per_word(word[:-1].lower(),'ham')
                
                probBeingSpam = priorSpam * wSpam
                probBeingHam = priorHam * wHam
                
            else:
                wSpam = probability_per_word(word.lower(),'spam')
                wHam = probability_per_word(word.lower(),'ham')
                
                probBeingSpam = priorSpam * wSpam
                probBeingHam = priorHam * wHam    
    
    #Get probability of message being spam 
    finalProb = probBeingSpam / (probBeingSpam + probBeingHam)
    msgText = "The text has a probability of: " +str(round(finalProb,6)) + "to be a spam."
    messagebox.showinfo("Probability of spam", msgText)

    
if __name__ == "__main__":
    root = Tk()
    root.title("Spam Detector")
    root.geometry("500x300")
    root.resizable(False,False)
    
    message = StringVar()
    
    label_frame = Frame(root,width=500,height=40)
    label_frame.pack_propagate(0) # Stops child widgets of label_frame from resizing it
    Label(label_frame,fg="black",text="Write the message that you want to validate:").pack()
    label_frame.place(x=8,y=10)
    
    text_frame = Frame(root,width=400,height=200)
    text_frame.pack_propagate(0) # Stops child widgets of label_frame from resizing it
    text_input = Text(text_frame,bg="white",fg="black",width=400,height=200)
    text_input.pack()
    text_frame.place(x=50,y=40)
    
    continue_button_frame = Frame(root)
    Button(continue_button_frame,text="Continuar",width=12,cursor="hand2",command=lambda:validate_text(text_input.get("1.0","end-1c"))).pack()
    continue_button_frame.place(x=210,y=260)
    
    root.mainloop()
