import wikipediaapi
import requests
from bs4 import BeautifulSoup as bs
import os
from os import path

def welcome(): #welcome function to get language

    global targetLanguage

    # WELCOME SCREEN
    print("[+] Welcome to Another Wordlist Provider (AWP) [+]")
    print("WIP! HERE SHOULD BE A NICE ASCII LOGO ︻デ═一")

    targetLanguage = input("[?] What is the target's language? (ISO 639-1): ").lower()
    while len(targetLanguage) != 2:
        targetLanguage = input("[!] Please input a 2-letter language code, such as \"en\": ")
    if not supportedLanguages(targetLanguage):
        print("[-] Sorry, language not supported! Defaulting to English...")
        targetLanguage = "en"
        listBuilder(targetLanguage)
    else:
        listBuilder(targetLanguage)

def supportedLanguages(targetLanguage):

    # PLACEHOLDER!
    # in reality would check github supported languages

    if targetLanguage in ["en", "fi"]:
        return True
    else:
        return False

def listBuilder(targetLanguage):

    awpList = []

    existingListQuery = input("[?] Do you want to use your own or community provided lists as a base? Y/[N]: ").lower()
    if existingListQuery == "y":
        while True:
            existingList = listSelector(targetLanguage)
            if not existingList:
                print("[+] Lists added as a base for", len(awpList), "words")
                break
            else:
                awpList.extend(existingList)
                existingListQuery = input("More lists? Y/[N]: ").lower()
                if existingListQuery == "y":
                    continue
                else:
                    print("[+] Lists added as a base for", len(awpList), "words")
                    break
    else:
        print("[+] Not using a base list")

    wikiListQuery = input("[?] Do you want to scrape Wikipedia for keywords? Y/[N]: ").lower()
    if wikiListQuery == "y":
        wikiList = wikiScraper(targetLanguage)
        awpList.extend(wikiList)
        print("Scraped Wiki in this language: ", targetLanguage)
        print(len(wikiList), " words added.")
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
        print("Added details about the target for", len(targetList), "words")

    print(awpList)

def listSelector(targetLanguage):

    print(
        "[1] Download an existing list from testhub.com\n[2] Use an existing local list\n[3] Nevermind")
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

    # PLACEHOLDER !

    if targetLanguage == "fi":
        downloadedList = ["salasana", "salasana2", "salasana3"]
    elif targetLanguage == "en":
        downloadedList = ["password", "password2", "password3"]
    else:
        downloadedList = ["Error 2 with language!"]
    return downloadedList

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

    # PLACEHOLDER !

    if targetLanguage == "fi" or targetLanguage == "en":
        scrapedWikiData = ["Game", "of", "Thrones"]
    else:
        scrapedWikiData = ["Error with language!"]
    return scrapedWikiData

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
                socialMediaSite = input("Do you wish to scrape more social medias? [Y]/N: ").lower()
                if socialMediaSite == "n":
                    break
                else:
                    continue

        if socialMediaSite == "2":
            socialMediaData = twitterScraper()
            if socialMediaData:
                socialMediaList.extend(socialMediaData)
                print("[+] Twitter scraped for a total of", len(socialMediaData), "words")
                socialMediaSite = input("Do you wish to scrape more social medias? [Y]/N: ").lower()
                if socialMediaSite == "n":
                    break
                else:
                    continue

        if socialMediaSite == "3":
            socialMediaData = instagramScraper()
            if socialMediaData:
                socialMediaList.extend(socialMediaData)
                print("[+] Instagram scraped for a total of", len(socialMediaData), "words")
                socialMediaSite = input("Do you wish to scrape more social medias? [Y]/N: ").lower()
                if socialMediaSite == "n":
                    break
                else:
                    continue
    return socialMediaList

def facebookScraper():
    facebookUsername = input("Please enter username: ")
    return ["Facebook", "True", facebookUsername]

def twitterScraper():
    twitterUsername = input("Please enter username: ")
    return ["Twitter", "True", twitterUsername]

def instagramScraper():
    instagramUsername = input("Please enter username: ")
    return ["Instagram", "True", instagramUsername]

def targetListBuilder():

    targetList = []

    print("[+] Press Enter for empty: ")

    targetName = input("[?] Enter target's full name: ").lower().split()
    targetSo = input("[?] Enter target's significant other's full name: ").lower().split()
    targetKeywords = input("[?] Enter keywords about the target (separated by spaces): ").lower().split()
    targetList.extend(targetName + targetSo + targetKeywords)

    return targetList

if __name__ == '__main__':
    welcome()