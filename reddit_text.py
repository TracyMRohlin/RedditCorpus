#!/usr/bin/env python

__author__ = 'girllunarexplorer'

import random
import sys
import os
import re
import datetime

from collections import OrderedDict
from pprint import pprint

import praw
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from create_scores_csv import calculate_karma
from make_time_interval import make_time_interval, extract_date


user_agent = "Thesis project by /u/girllunarexplorer"
r = praw.Reddit(user_agent=user_agent)

class RedditText(object):
    """Creates a Reddit object so that the user can retrieve posts or comments from Reddit.
    If a subreddit is not provided, the subreddit will be randomly selected.
    The minimum length for words in a post is set to 25 in order to filter picture oriented subreddits."""

    def __init__(self):
        super(RedditText, self).__init__()
        self.first = None
        self.last = None
        self.loc = None
        self.save = None
        self.subreddit = None
        self.min_length = 20

        self.stops = stopwords.words('english')
        # the nltk stopwords list isn't all inclusive (it mostly excludes contractions)
        # so to make it more comprehensive i've added more stopwords
        # following the list at http://www.ranks.nl/stopwords
        self.stops.extend(["against", 'cannot', 'could', 'he', "ought", "would"])
        self.stops = set(self.stops)

        self.function_call = ""
        self.posts = []


    def get_subreddit(self, subreddit):
        """Sets the subreddit to be looked at based on user input or randomization.
        Later, if submissions() turns up an empty list (which likely indicates an
        image based sub), get_subreddit is called again."""
        # user can provide a specific subreddit or have one randomly provided
        try:
            if not subreddit:
                self.subreddit = r.get_random_subreddit()
            else:
                self.subreddit = r.get_subreddit(subreddit)
            print "Current subreddit is " + str(self.subreddit) + "\n"



            # asks the user where to save the corpus files
            response = raw_input("Would you like to save as text files? [y/n]\n").lower().strip()[0]
            if response == "y":
                self.save = True
                default_loc = "/Users/tracyrohlin/PycharmProjects/RedditCorpus_copy/{}/".format(self.subreddit)
                self.loc = raw_input("Press ENTER to use default, otherwise enter location."
                                    "\nThe default location is: " + default_loc +"\n")
                if not self.loc:
                    self.loc = default_loc

                # Set the current directory to what the user specifies
                if not os.path.exists(self.loc):
                    os.mkdir(self.loc)
                os.chdir(self.loc)

        except Exception as error:
            print error
            print "Trouble connecting. Please try again."


    def submissions(self, n):
        """Grabs all the posts from a subreddit within the time period of one year from current date to a month
        before current date.  This is done in order to make sure that all the posts have had sufficient time to be
        voted upon."""
        assert n > 0, "The number of posts must be more than zero."

        if not self.last:
            self.first, self.last = extract_date(self.loc)

        else:
            self.first, self.last = make_time_interval(self.first)

        # create a timestamp query and search in that specific subreddit
        query = 'timestamp:%d..%d' % (self.first, self.last)
        submissions = r.search(query, subreddit=self.subreddit, sort="new", limit=None, syntax='cloudsearch')

        # Make sure that the posts actually have a sufficient amount of text in them and have at least 1 point each
        res = []

        for submission in submissions:
            if len(res) < n:
                if len(submission.selftext.lower()) >= self.min_length and submission.score > 1:

                    res.append((submission.title, submission))
            else:
              break



        # Sometimes the amount of submissions grabbed is small due to it having an excessive amount of images or links
        # as posts.  There may be a few text based post in the result, however, so the program asks if the user
        # wants to continue with the less than desired amount of posts
        if len(res) < n:
            if len(res) != 0:
                diff = n - len(res)
                response = raw_input("The amount of submissions grabbed was less than requested by {} posts, "
                                     "do you wish to proceed in processing text? [y/n]\n".format(diff))
                if response[0].lower().strip() == "y":
                    return res
                else:
                    sys.exit(0)

            print "Sorry, r/{} appears to be an image heavy subreddit.".format(self.subreddit)
            response = raw_input("Please provide another subreddit or press ENTER for a random subreddit.\n"
                                 ">> ").strip()
            self.get_subreddit(response)
            self.submissions(n)

        return res


    def get_all_posts(self):
        """Grabs n posts from the subreddit and saves them as corpus files."""
        self.scores = [] # Save scores into this list because it will be used  when saving the submission
        post = ""
        i=1
        # Collect all the text from the posts to return later as a corpus file or in terminal.
        for p in self.posts:
            print "\nWorking on post #{}...".format(i)
            score = p[-1].score
            post_body = "Title: {0}\n" \
                        "Karma: {1}\n" \
                        "Date: {2}\n" \
                        "{3}{4}".format(self.token_and_tag(p[0]), score, p[-1].created,
                                                         self.token_and_tag(p[-1].selftext),
                                                         "\n"*2)
            post_body += "="*30 +"\n\n"
            post += post_body
            self.scores.append(score)

            if self.save and self.function_call != "cp":
            # Checks to see that it is not being called by combine_texts(), which would save the text in one
            # large corpus file. If this check were not implemented, combine_texts() would end up saving three separate
            # files: one for when get_all_posts() is called, one for when get_all_comments() is called, and another
            # for when combine_texts() is called.
                self.save_submissions(post_body, karma=score, iteration=i)
            else: pass

            i+=1

        # the csv of all Karma scores will only be saved if the user specifies where to save the corpus files
        if self.loc:
            self.scores.sort()
            calculate_karma(self.subreddit, self.scores, "Karma Scores")
        #return "\nRetrieved posts:\n\n" + post


    def get_all_comments(self):
        """Grabs comments from n posts and saves them as corpus files."""

        scores = []
        posts = [p[1] for p in self.posts]
        total_comments = ""

        i = j = 1
        # creates a long text block with all the comments from a single post that is either saved in a corpus file or
        # returned in terminal
        for p in posts:
            total_comments += "Comments from post:\n"
            j += 1
            print "Working on getting comments and flattening the comment tree..."
            # to make praw.replace_more_comments more efficient, the limit and threshold is set at 10, meaning that
            # it will make only 10 additional requests, and only make requests that give back 10 additional comments.
            # This is limited because each request requires a 2 second delay by PRAW and if no limits are set, the program
            # will become very slow.
            p.replace_more_comments(limit=10, threshold=5)
            coms = praw.helpers.flatten_tree(p.comments)
            for c in coms:
                print "\nWorking on comment #{}...".format(i)
                comment = self.token_and_tag(c.body)
                if comment:
                    score = c.score
                    total_comments += "New comment:\nKarma: {0}\n{1}\n\n".format(score, comment)
                    scores.append(score)
                i+=1
            total_comments += "\n"+"+"*30 +"\n"

            # saves all the comments from a post in one corpus file on a post by post basis
            if self.save and self.function_call != "cp":
                self.save_submissions(total_comments, karma=p.score)


        if self.function_call != "cp" and self.loc:
            print calculate_karma(self.subreddit, self.scores, "Karma Scores")

        return total_comments


    def combine_texts(self):
        """Combines posts and comments into one corpus file."""

        result = ""
        # the data has already been tagged so it must be split on the demarcator and zipped together to make sure
        # the comments coincide with the correct post
        posts = self.get_all_posts().split("="*30)[:-1]
        comments = self.get_all_comments().split("+"*30)
        i = 0
        for p, c in zip(posts, comments):
            # creates a temporary result so that each post+comments can be saved as a separate corpus file
            # otherwise the result would be saved into one giant corpus file.
            p = re.sub(r"Retrieved posts:", "", p).strip()
            temporary_result = "New post:\n"
            body = "{}\n\n{}\n".format(p, c)
            temporary_result += body
            result = temporary_result

            if self.save:
                self.save_submissions(temporary_result, karma=self.scores[i])
            i += 1

        return result


    def get_random_post(self,n):
        """Grabs a random post from the top n posts in the same subreddit."""

        # appends all of the posts to a single list and then randomly choses the post tuple that contains the text,
        # score and title
        posts = []
        print "Working..."
        for p in self.subreddit.get_new(limit=n):
            body = p.selftext.lower()
            if body.split() >= self.min_length:
                posts.append((self.token_and_tag(body).strip(), p.score, p.title))

        only_post = random.choice(posts)
        text, score, title = only_post
        score = score

        # checks to see if the post actually has any text in it
        if not text:
            print "Sorry, this post appears to be an image.\n".format(self.subreddit)
            response = raw_input("Please provide another subreddit or press ENTER for a random subreddit.\n"
                                 ">> ").strip()
            self.get_subreddit(response)
            return self.get_random_post(n)

        res = "Title: {0}\nKarma: {1}\n\n{2}".format(title, score, text)

        if self.save:
            self.save_submissions(text, karma=score)

        return "\nRetrieved random post:\n\n" + res + "\n"


    def get_random_comment(self, n):
        """Grabs a random comment from the same subreddit."""

        try:
            comments = []
            for p in self.subreddit.get_new(limit=n):
                print "Working..."
                p.replace_more_comments(limit=10, threshold=5) # removes the "moreComments" objects and returns them as actual comments
                for c in praw.helpers.flatten_tree(p.comments):
                    body = c.body
                    if body.split() >= self.min_length:
                        comments.append([self.token_and_tag(body), c.score])

            only_post, score = random.choice(comments)
            score = score

            if self.save:
                self.save_submissions(only_post, karma=score)

            if not only_post:
                print "This comment was an image and had a karma score of {}.  Trying again...".format(score)
                return self.get_random_comment(n)

            res = "\nRetrieved random comment:\n"
            res += "Karma: {} \n\n{}".format(score, only_post) + "\n"
            return res

        except Exception as error:
            print error
            print "No comments were found among new posts"


    def token_and_tag(self, text):
        """Returns clean texts and tokenizes it."""
        text += "\t" # add a tab to make sure that the re.sub() successfully removes any links at the end of the text block
        newtext = self.remove_unwanted(text)
        tagged = []
        tokens = newtext.split()
        for word in tokens:
            try:
                word = word.encode("utf-8").lower()
                if word in self.stops:
                    continue
                tagged.append(word)
            except:
                print "Was unable to tag word due to unknown ASCII character."
        return " ".join(tagged)


    def remove_unwanted(self, text):

        text = re.sub(r"u\/.*[\s\t]*" # removes mentions to other redditors as well as contractions
                      r"|\w+'\w+|\w+'[A-Za-z]?"    # removes contractions like "don't" and "can't" from the text
                      r"|\\u000a"      # removes anonymized usernames from text
                      r"|\[deleted\]" # removes the deleted tag
                      r"|http.*[\s\t]", "", text) # removes links from text
        new = re.sub(r"[^A-Za-z\t\s\']*", "", text) # removes all punctuation from the document
        return new



    def save_submissions(self, text, karma=None, iteration=None):
        """Iteration labels the files "1_subreddit_date", "2_subreddit_date", etc.
        to make it easier to distinguish separate posts from the same subreddit."""

        # Considering the files are saved in quick succession, it is easier to delineate files if they are
        # saved with an iteration number
        if iteration:
            file_name = "{}_{} Karma {} - {}.txt".format(iteration, str(self.subreddit), karma, str(datetime.datetime.now()))
        else:
            file_name = "{} Karma {} - {}.txt".format(str(self.subreddit), karma, str(datetime.datetime.now()))


        with open(os.path.join(".", file_name), "wb") as file:
            file.write(text)
            print "Saved entry into a corpus file."


    def print_func(self, function, n=None):
        try:
            if n:
                print function(n)
            else:
                print function()
        except Exception as e:
            print e


def start_up():
    """Creates a RedditText class object and asks the user if they would like to get all posts, all comments, a random
    comment or random post."""
    new = RedditText()
    subreddit = raw_input("What subreddit would you like to grab posts from?"
                          "\nTo grab a random subreddit, press ENTER.\n>> ")
    new.get_subreddit(subreddit)


    menu = OrderedDict([
        ("cp", new.combine_texts),
        ("ap", new.get_all_posts),
        ("ac", new.get_all_comments),
        ("rp", new.get_random_post),
        ("rc", new.get_random_comment)
    ])


    def menu_loop():
        """Show the menu"""

        choice = None
        while choice != "q":
            print "Enter 'q' to quit."
            for key, value in menu.items():
                print "[{}] {}".format(key, value.__doc__)

            choice = raw_input("Action:  ").lower().strip()
            # checks to see if the choice is valid given the options
            if choice in menu:
                new.function_call = choice
                n = raw_input("How many posts would you like to grab?\n")
                try:
                    n = int(n)
                except ValueError:
                    print "That is not a valid number."
                if choice in ["cp", "ap", "ac"]:
                    new.posts = [p for p in new.submissions(n)]
                    new.print_func(menu[choice])
                # calls the random post or random comment functions
                else:
                    new.print_func(menu[choice], n)
            elif choice[0] == "q":
                break
            else:
                 print "That is not a valid menu option."
    menu_loop()

if __name__ == "__main__":
    start_up()
