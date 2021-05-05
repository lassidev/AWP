import wikipedia
import wikipediaapi
import twint
import requests
from bs4 import BeautifulSoup as bs
import re
import os
import sys
from os import path
from github import Github
from pathvalidate import sanitize_filename
from colorama import Fore, Style, init
from termcolor import colored

g = Github("") #github token API, remove before push
init(autoreset=True) #colorama init

def generator():

    list = welcome()
    expander(list)

def welcome(): #welcome function to get language

    global targetLanguage

    # WELCOME SCREEN
    print(colored("[+] Welcome to Another Wordlist Provider (AWP) [+]", "green"))
    print("""                                                                                                                                                                                                                      
..................................NN........... ....................................................
.......................DMNNMNNNDMMNDN8NNDNNN8$Z.....................................................
.......................NMMMMMMMNMMNMMNMMMMMMNNN ....................................................
............................. .NO.. .NM. ...... ....................................................
.    .....................NNNDD8DNDNNDNDNONDDDD888OOOOOO8OZZOOOOOOOO888888DDDDDDDDDNDDNNNNNNMMNMNN..
.DDDDMM$$$D8D88888DDDDDDDNZO8DD888ZZZ78888O??ZOOOZ$Z8OO8DDM.......................... ......NN .....
.NNNNNNDDZ$OD8OZ$O888D87DDD8DO888DDDODDDDDDDNNNN8NNNNNNNNNN.........................................
.NNNNDNNNNNNNN8NNN.....NNM.:..DNDDDNNNDNN..............88O88ND87DD?~~~~,ND..........................
.MNNNNNNNNNNNNNNNM....MMNM....Z.DDNNND .............................................................
.NNNNNNNNM....MMMMMMMMMMM .......   ................................................................
.DDD8MMMMN.....MMMMMMMMMM...........................................................................
.....................,~8,...........................................................................                                                                                                                                  
                                                                         
    """)

    targetLanguage = input(colored("[?] What is the target's language? (ISO 639-1): ", "cyan")).lower()
    while len(targetLanguage) != 2:
        targetLanguage = input("[!] Please input a 2-letter language code, such as \"en\": ").lower()
    if not supportedLanguages(targetLanguage):
        print("[-] Sorry, language not supported! Defaulting to English...")
        targetLanguage = "en"
        return listBuilder(targetLanguage)
    else:
        return listBuilder(targetLanguage)


def listBuilder(targetLanguage):

    awpList = []

    existingListQuery = input("[?] Do you want to use your own or community provided lists as a base? Y/[N]").lower()
    if existingListQuery == "y":
        while True:
            existingList = listSelector(targetLanguage)
            if not existingList:
                print("[+] Lists added as a base for", len(awpList), "words")
                break
            else:
                awpList.extend(existingList)
                existingListQuery = input("[?] More lists? Y/[N]: ").lower()
                if existingListQuery == "y":
                    continue
                else:
                    print(colored("[+] Lists added as a base for", "green"), colored(len(awpList), "red"), "words")
                    break
    else:
        print("[+] Not using a base list")

    wikiListQuery = input("[?] Do you want to scrape Wikipedia for keywords? Y/[N]: ").lower()
    if wikiListQuery == "y":
        wikiList = wikiScraper(targetLanguage)
        awpList.extend(wikiList)
        print("[+]", len(wikiList), " words added.")
    else:
        print("[+] Not scraping Wikipedia.")

    webListQuery = input("[?] Do you want to scrape a website (e.g. workplace or university) for keywords? Y/[N]: ").lower()
    if webListQuery == "y":
        webList = websiteScraper()
        if webList:
            awpList.extend(webList)
            print("[+] Scraped website,", len(webList), " words")
        else:
            print("[!] Error scraping website")
    else:
        print("[+] Not scraping additional websites.")

    socialMediaListQuery = input("[?] Do you want to scrape public social media accounts for keywords? Y/[N]: ").lower()
    if socialMediaListQuery == "y":
        socialMediaList = socialMediaScraper()
        if socialMediaList:
            awpList.extend(socialMediaList)
            print("[+] Scraped social medias for a total of", len(socialMediaList), " words")
        else:
            print("[!] Error scraping social medias")
    else:
        print("[+] Not scraping social medias.")

    targetListQuery = input("[?] Do you want to add manual details about the target? [Y]/N: ").lower()
    if targetListQuery == "n":
        print("[+] Not adding manual details")
    else:
        targetList = targetListBuilder()
        awpList.extend(targetList)
        print("[+] Added details about the target for", len(targetList), "words")

    return awpList

def expander(list):

    #needs functionality to:
    #1. show word count and file size
    #2. actually expand the dictionary with rules (1337 mode, special chars, etc)
    #3. select what file to write in

    fullPath = fileinput()

    print("[+] The wordlist contains", len(list), "words")
    print("[+] The size of the wordlist is", sys.getsizeof(list), "bytes")
    with open(fullPath, mode='x', encoding='utf-8') as myfile:
        myfile.write('\n'.join(list))
        myfile.write('\n')
    print("[+] Wordlist successfully saved to", fullPath)

def fileinput():

    while True:
        fileLocation = input("[?] Where do you want to write the file? (defaults to working directory if empty): ")
        if fileLocation == "":
            fileLocation = os.getcwd()
            break
        else:
            if os.path.isdir(fileLocation):
                break
            else:
                print("[!] Directory doesn't exist!")
                continue
    if fileLocation[-1] != "/":
        fileLocation += "/"

    fileNameInput = input("[?] What is the name of the file? (defaults to wordlist.txt if empty): ")
    if fileNameInput == "":
        fileNameInput = "wordlist"
    fileName = sanitize_filename(fileNameInput)
    if not fileName.endswith(".txt"):
        fullPath = fileLocation + fileName + ".txt"
    else:
        fullPath = fileLocation + fileName

    return fullPath

def supportedLanguages(targetLanguage):

    # PLACEHOLDER!
    # in reality would check github supported languages

    if targetLanguage in ["en", "fi"]:
        return True
    else:
        return False

def listSelector(targetLanguage):

    print(
        "[1] Download an existing list from github\n[2] Use an existing local list\n[3] Nevermind")
    listOption = input("[?] Choose an option: ")

    while listOption not in ("1", "2", "3"):
        listOption = input("[?] Please select a valid option (1, 2, 3): ")

    if listOption == "1":
        listOption = downloadList(targetLanguage)
        print("[+] Done downloading lists!")
        return listOption

    elif listOption == "2":
        listOption = getLocalList()
        tmpLocalList = []
        if listOption:
            with open(listOption, 'r') as f:
                tmpLocalList.extend(line.strip() for line in f)
            pass
        print("[+] Done adding local list!")
        return tmpLocalList

    elif listOption == "3":
        return False

def downloadList(targetLanguage):

    wordlists = {} #init wordlist option dictionary
    i = 0
    repo = g.get_repo("lassidev/AWP") #my repo
    contents = repo.get_contents("wordlists/{}".format(targetLanguage)) #get list of all files in wordlist directory
    print("[?] Which wordlist do you wish to use?")
    for content_file in contents:
        i += 1
        stripped_content_file = str(content_file).replace("ContentFile(path=\"", "").replace("\")", "") #convert ObjectFile to string and strip unnecessary characters
        wordlists[i] = stripped_content_file #add options to dictionary with key values, starting from 1
        print("[{}]".format(i), stripped_content_file) #print options
    while True:
        selection = input("[?] Which wordlist do you want to use?: ")
        if int(selection) <= i:
            break
        else:
            print("[!] Please input valid selection!")
            continue
    f = repo.get_contents(wordlists[int(selection)])
    raw_data = f.decoded_content
    downloadedList = str(raw_data, "utf-8")
    print("[+] Downloaded a wordlist containing", downloadedList.count("\n"), "words")
    return downloadedList.split()

def getLocalList():

    localList = input("[?] Please input location of existing list: ").lower()
    while not path.isfile(localList):
        localList = input("[?] File doesn't exist. Please input correct file or type \"nvm\" to abort: ")
        if localList == "nvm":
            break
    if localList != "nvm":
        print("[+] Adding existing list...")
        return localList
    else:
        return False

def wikiScraper(targetLanguage):

    wikiData = []

    while True:
        pageInput = input("[?] Enter the name of the Wikipedia page: ")
        pageChecker = wikipediaapi.Wikipedia(targetLanguage)
        if pageChecker.page(pageInput).exists():
            wikiPage = wikipedia.page(pageInput)
            wikiData.extend(wikiPage.content.split(" "))
            print("[+]", len(wikiData), "words scraped from Wikipedia")
            pageInput = input("[?] Do you want to add another page? Y/[N]: ").lower()
            if pageInput == "y":
                continue
            else:
                break
        else:
            print("[!] Wikipedia page not found! Here's the results found with that term: ")
            print(wikipedia.search(pageInput))
            continue
    return wikiData


def websiteScraper():

    # PLACEHOLDER !
    # cewl or wget or something, return list of website words

    websiteUrl = input("[?] Please input website url: ")
    websiteWords = ["Lorem", "Ipsum"]
    return websiteWords

def socialMediaScraper():

    # PLACEHOLDER !
    # need apis for social media scraping (instagram comments, twitter likes, etc)

    socialMediaList = []
    socialMediaOptions = "[1] Facebook\n[2] Twitter\n[3] Instagram\n[4] Nevermind"
    while True:
        print(socialMediaOptions)
        socialMediaSite = input("[?] Choose an option: ")

        while socialMediaSite not in ("1", "2", "3", "4"):
            print(socialMediaOptions)
            socialMediaSite = input("[?] Please select a valid option (1, 2, 3, 4): ")

        if socialMediaSite == "1":
            socialMediaData = facebookScraper()
            if socialMediaData:
                socialMediaList.extend(socialMediaData)
                print("[+] Facebook scraped for a total of", len(socialMediaData), "words")
                socialMediaSite = input("[?] Do you wish to scrape more social medias? [Y]/N: ").lower()
                if socialMediaSite == "n":
                    break
                else:
                    continue

        if socialMediaSite == "2":
            socialMediaData = twitterScraper()
            if socialMediaData:
                socialMediaList.extend(socialMediaData)
                print("[+] Twitter scraped for a total of", len(socialMediaData), "words")
                socialMediaSite = input("[?] Do you wish to scrape more social medias? [Y]/N: ").lower()
                if socialMediaSite == "n":
                    break
                else:
                    continue

        if socialMediaSite == "3":
            socialMediaData = instagramScraper()
            if socialMediaData:
                socialMediaList.extend(socialMediaData)
                print("[+] Instagram scraped for a total of", len(socialMediaData), "words")
                socialMediaSite = input("[?] Do you wish to scrape more social medias? [Y]/N: ").lower()
                if socialMediaSite == "n":
                    break
                else:
                    continue
    return socialMediaList

def facebookScraper(): #needs actual scraping function
    facebookUsername = input("[?] Please enter username: ")
    return ["Facebook", "True", facebookUsername]

def twitterScraper(): #needs actual scraping function
    #could some interest algorithm be used to generate list? For example, if user follows lot of bitcoin blogs

    tweets = [] #init list for scraped tweets
    tweetsStripped = [] #init list for formatted words from tweets

    c = twint.Config() #using twint config
    c.Username = input("[?] What is the target's username?: ").lower()
    while True:
        try:
            c.Limit = int(input("[?] How many tweets do you want to scrape? (minimum 100): ")) #twint always scrapes minimum 100 tweets
            break
        except:
            print("[!] That's not a number!")
    while True:
        try:
            charactercount = int(input("[?] What is the minimum character length of words you want to be added to the list?: ")) #only include words that are >= x length
            break
        except:
            print("[!] That's not a number!")
    c.Store_object = True #store scraped objects in RAM (needed in twint)
    c.Store_object_tweets_list = tweets #store tweets in list
    c.Hide_output = True
    twint.run.Search(c)

    for i in range(len(tweets)):
        splitTweet = tweets[i].tweet.split() #split each tweet into words

        for words in splitTweet:
            if len(words) >= charactercount and "http" not in words and "@" not in words: #charactercount, remove links and username mentions
                cleanedWord = re.sub('[^A-Za-z0-9]+', '', words) #strip special characters (needs work)
                tweetsStripped.append(cleanedWord)

    return tweetsStripped #return ready list

def instagramScraper(): #needs actual scraping function
    instagramUsername = input("[?] Please enter username: ")
    return ["Instagram", "True", instagramUsername]

def targetListBuilder():

    targetList = []

    print("[+] Press Enter for empty: ")

    # Needs more questions (refer to CUPP)

    targetName = input("[?] Enter target's full name: ").lower().split()
    targetSo = input("[?] Enter target's significant other's full name: ").lower().split()
    targetKeywords = input("[?] Enter keywords about the target (separated by spaces): ").lower().split()
    targetList.extend(targetName + targetSo + targetKeywords)

    return targetList

if __name__ == '__main__':
    generator()
