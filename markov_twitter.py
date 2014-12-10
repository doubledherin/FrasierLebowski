#!/usr/bin/env python

import os
import twitter
from sys import argv
import random
import string

def make_chains(corpus, num):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""

    new_corpus = "" 
    
    for char in corpus:

        # Leave out certain kinds of punctuation
        if char in "_*\"":
            continue
        
        # Keep everything else      
        else:
            new_corpus += char

    # Split the cleaned corpus into a list of words
    list_of_words = new_corpus.split()


    # Initialize the dictionary that will hold the Markov chains
    d = {}

    # Build chains, where the key (prefix) is a tuple 
    # and the value is a list of legal suffixes
    for i in range( (len(list_of_words) - num) ):
        
        prefix = []
        
        # Build a prefix of length num
        for j in range(num):

            prefix.append(list_of_words[i + j])
        
        prefix = tuple(prefix)
        
        suffix = list_of_words[i+num] 

        # Add to dictionary
        if prefix not in d:
            d[prefix] = [suffix]  # initializes the suffix as a list
        else:
            d[prefix].append(suffix)
            
    return d
        
def make_text(chains, num):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""

    # Create a list of chain's keys, then return one of the keys at random
    random_prefix = random.choice(chains.keys())

    # From the list of values for the chosen key, return one value at random
    random_suffix = random.choice(chains[random_prefix])
    
    # Initialize an empty string for our random text string
    markov_text = ""

    # Iterate over prefix's tuple and add each word to the random text string
    for word in random_prefix:
        markov_text += word + " "

    # Then add the suffix
    markov_text += random_suffix + " "

    # Rename random_prefix and random_suffix so that we can call them
    # in a the following for loop
    prefix = random_prefix
    suffix = random_suffix

    for i in range(30):

        # Create a new prefix from the last items in the most recent prefix and
        # the most recent suffix
        newprefix = []

        for j in range(1, num):
            newprefix.append(prefix[j])
        newprefix.append(suffix)
        prefix = tuple(newprefix)

        # Choose a random suffix from the new prefix's values
        suffix = random.choice(chains[prefix])

        # Add it all to the random text string
        markov_text += "%s " % (suffix)

    return markov_text

def tweetmash(markov_text):
    """Takes a randomly generated markovian string, creates a tweet-length substring, and tweets it.
    """
    # Split string into words
    words = markov_text.split()

    # Remove the first word until the first word is initial capped
    while words[0].istitle() == False:
        words.pop(0)

    # Remove the final words until the final words ends with end punctuation
    while words[-1][-1] not in ".!\"?'":
        words.pop()

    # Put the list back into a string and decrease len and recurse until it's <= 140
    tweet = (" ").join(words)
    if len(tweet) > 140:
        tweet = tweet[:138]
        tweetmash(tweet)
    else:
        if tweet != None:

            api = twitter.Api(consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
                              consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
                              access_token_key=os.environ.get('TWITTER_ACCESS_TOKEN'),
                              access_token_secret=os.environ.get('TWITTER_ACCESS_SECRET'))
            status = api.PostUpdate(tweet)
            print "Tweet tweeted!"
            return

def main():
    script, filename1, filename2, num = argv
    num = int(num)
    fin1 = open(filename1)
    input_text = fin1.read()
    fin2 = open(filename2)
    input_text += fin2.read()
    fin1.close()
    fin2.close()


    chain_dict = make_chains(input_text, num)
    random_text = make_text(chain_dict, num)
    random_tweet = tweetmash(random_text)



if __name__ == "__main__":
    main()