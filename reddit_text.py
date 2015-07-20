#!/usr/bin/env python

__author__ = 'girllunarexplorer'

import random
from re import sub
from datetime import datetime
from collections import OrderedDict
from pprint import pprint
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import os
import traceback
import praw
import nltk


user_agent = "Thesis project by /u/girllunarexplorer"
r = praw.Reddit(user_agent=user_agent)

class RedditText(object):
    """Creates a Reddit object so that the user can retrieve posts or comments from Reddit.
    If a subreddit is not provided, the subreddit will be randomly selected.
    The minimum length for words in a post is set to 25 in order to filter picture oriented subreddits."""

    def __init__(self):
        super(RedditText, self).__init__()
        self.save = None
        self.subreddit = None
        self.min_length = 25
        self.stemmer = WordNetLemmatizer()
        self.stops = stopwords.words('english')
        self.function_call = ""
        self.log = False
        self.posts = []


    def get_subreddit(self, subreddit):
        """Sets the subreddit to be looked at based on user input or randomization.
        Later, if submissions() turns up an empty list (which likely indicates an
        image based sub), get_subreddit is called again."""
        try:
            if not subreddit:
                self.subreddit = r.get_random_subreddit()
            else:
                self.subreddit = r.get_subreddit(subreddit)

            print "Current subreddit is " + str(self.subreddit)+ "\n"
            try:
                self.top_posts = self.subreddit.get_top_from_all()
            except Exception as error:
                print error
            response = raw_input("Would you like to save as text files? [y/n]\n").lower().strip()[0]
            if response[0].lower() == "y":
                self.save = True
                default_loc = "/Users/GirlLunarExplorer/PycharmProjects/RedditCorpus/{}/".format(self.subreddit)
                self.loc = raw_input("Press ENTER to use default, otherwise enter location."
                                    "\nThe default location is: " + default_loc +"\n")
                if not self.loc:
                    self.loc = default_loc

                log = raw_input("Would you like to log all the untagged words? [y/n]\n")
                if log[0].lower() == "y":
                    self.log = True

        except Exception as error:
            print error
            print "Trouble connecting. Please try again."


    def try_unicode(self, text):
        new =[]
        untagged = []
        text = self.remove_unwanted(text)
        for word in text.split():
            try:
                new.append(word.encode("utf-8").lower())
            except:
                untagged.append(untagged)

        if untagged and self.log == True:
            ut_words = " ".join(untagged)
            self.save_submissions(ut_words, Log=True)
        return self.token_and_tag(" ".join(new))


    def token_and_tag(self, text):
        untagged = []
        tagged = []
        tokens = text.split()
        for word in tokens:
            try:
                word = word.encode("utf-8").lower()
                if word in self.stops:
                    continue

                word, tag = nltk.pos_tag([word])[0]
                pos = tag[0].lower()
                if pos in ["a", "n", "v"]:
                    word = self.stemmer.lemmatize(word, pos=pos)
                tagged.append("/".join([word, tag]))
            except:
                print "Was unable to tag word due to unknown ASCII character."
                untagged.append(word)

        if untagged and self.log == True:
            ut_words = " ".join(untagged)
            self.save_submissions(ut_words, Log=True)

        return " ".join(tagged)


    def remove_unwanted(self, text):
        try:
            text = sub(r"\\u000a", "", text) # removes usernames from text
            text = sub(r"\[deleted\]", "", text) # removes [deleted] from text
            text = sub("\[[\w+\s+]*\]\(.*\)", "", text) # removes links from text
            text = sub('"', '', text) # removes punctuation
            text = sub("'", '', text) # removes punctuation
            return text
        except Exception as e:
            print e



    def submissions(self, n):
        """Grabs all the top posts from a subreddit."""

        min_score = 20
        assert n > 0, "The number of posts must be more than zero."
        res = []
        for submission in self.top_posts:
            if len(res) < n:
                if len(submission.selftext.lower()) >= self.min_length and submission.score >= min_score:
                    res.append((submission.title, submission))
            else:
                break
        if len(res) < n:
            if len(res) != 0:
                diff = n - len(res)
                response = raw_input("The amount of submissions grabbed was less than requested by {} posts, "
                                     "do you wish to proceed in processing text? [y/n]\n".format(diff))
                if response[0].lower().strip() == "y":
                    return res

            print "Sorry, r/{} appears to be an image heavy subreddit.".format(self.subreddit)
            response = raw_input("Please provide another subreddit or press ENTER for a random subreddit.\n"
                                 ">> ").strip()
            self.get_subreddit(response)
            self.submissions(n)
        return res


    def save_submissions(self, text, iteration=None, Log=False):
        """Labels file "1_subreddit_date", "2_subreddit_date", etc.
        to make it easier to distinguish separate posts from the same subreddit."""

        if iteration:
            file_name = "{}_{} - {}.txt".format(iteration, str(self.subreddit), str(datetime.now()))
        elif Log:
            file_name = "Untagged: {} - {}.txt".format(str(self.subreddit), str(datetime.now()))
        else:
            file_name = "{} - {}.txt".format(str(self.subreddit), str(datetime.now()))

        if not os.path.exists(self.loc):
            os.mkdir(self.loc)
        with open(os.path.join(self.loc, file_name), "wb") as file:
            print "Working..."
            file.write(text)
            print "Saved entry into a corpus file."


    def get_all_posts(self):
        """Grabs n posts from the subreddit and saves them as corpus files."""

        post = ""
        i=1
        for p in self.posts:
            print "\nWorking on post #{}...".format(i)
            post_body = "Title: {0}\nKarma: {1}\n{2}{3}".format(self.try_unicode(p[0]),
                                                         p[-1].score,
                                                         self.try_unicode(p[-1].selftext.lower()),
                                                         "\n"*2)
            post += post_body
            post += "="*30 +"\n\n"

            if self.save and self.function_call != "ga":
            # Checks to see that it is not being called by combine_texts(), which would save the text in one
            # large corpus file. If this check were not implemented, combine_texts() would end up saving three separate
            # files: one for when get_all_posts() is called, one for when get_all_comments() is called, and another
            # for when combine_texts() is called.
                self.save_submissions(post, i)
            else: pass

            i+=1

        return "\nRetrieved posts:\n\n" + post


    def get_all_comments(self):
        """Grabs comments from n posts and saves them as corpus files."""
        posts = [p[1] for p in self.posts]
        total_comments = ""

        i = j = 1
        for p in posts:
            total_comments += "Comments from post:\n"
            j += 1
            p.replace_more_comments(limit=None)
            coms = praw.helpers.flatten_tree(p.comments)
            for c in coms:
                print "\nWorking on comment #{}...".format(i)
                comment = self.try_unicode(c.body)
                if comment:
                    total_comments += "New comment:\nKarma: {0}\n{1}\n\n".format(c.score, comment)
                i+=1
            total_comments += "\n"+"+"*30 +"\n"

            if self.save and self.function_call != "ga":
                self.save_submissions(total_comments)

        return total_comments


    def combine_texts(self):
        """Combines posts and comments into one corpus file."""

        result = ""
        # the data has already been tagged so it must be split on the demarcator
        posts = self.get_all_posts().split("="*30)[:-1]
        comments = self.get_all_comments().split("+"*30)
        for p, c in zip(posts, comments):
            p = sub(r"Retrieved posts:", "", p).strip()
            result += "New post:\n"
            body = "{}\n\n{}\n".format(p, c)
            result += body

        if self.save:
            self.save_submissions(result)

        return result


    def get_random_post(self,n):
        """Grabs a random post from the top n posts in the same subreddit."""

        posts = []
        print "Working..."
        for p in self.subreddit.get_new(limit=n):
            body = p.selftext.lower()
            if body.split() >= self.min_length:
                posts.append((self.try_unicode(body).strip(), p.score, p.title))

        only_post = random.choice(posts)
        text, score, title = only_post


        if not text:
            print "Sorry, this post appears to be image based.\n".format(self.subreddit)
            response = raw_input("Please provide another subreddit or press ENTER for a random subreddit.\n"
                                 ">> ").strip()
            self.get_subreddit(response)
            return self.get_random_post(n)

        if score >=30:
                text += "\n{} is a popular post.\n".format(title)

        res = "Title: {0}\nKarma: {1}\n\n{2}".format(title, score, text)

        if self.save:
            self.save_submissions(text)

        return "\nRetrieved random post:\n\n" + res + "\n"


    def get_random_comment(self, n):
        """Grabs a random comment from the same subreddit."""
        try:
            comments = []
            for p in self.subreddit.get_new(limit=n):
                print "Working..."
                p.replace_more_comments(limit=None) #removes the "moreComments" objects and returns them as actual comments
                for c in praw.helpers.flatten_tree(p.comments):
                    body = c.body
                    if body.split() >= self.min_length:
                        comments.append([self.try_unicode(body), c.score])

            only_post, score = random.choice(comments)

            if self.save:
                self.save_submissions(only_post, score)
            if not only_post:
                return "This comment was an image and had a karma score of {}".format(score)
            res = "\nRetrieved random comment:\n"
            res += "Karma: {} \n\n{}".format(score, only_post) + "\n"
            return res

        except Exception as error:
            print error
            print "No comments were found among new posts"


    def print_func(self, function, n=None):
        try:
            if n:
                print function(n)
            else:
                print function()
        except Exception as e:
            print e


def start_up():
    subreddit = raw_input("What subreddit would you like to grab posts from?"
                          "\nTo grab a random subreddit, press ENTER.\n>> ")
    new = RedditText()
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
            if choice in menu:
                new.function_call = choice
                n = raw_input("How many posts would you like to grab?\n")
                try:
                    n = int(n)
                except:
                    print "That is not a valid number."
                if choice in ["cp", "ap", "ac"]:
                    new.posts = [p for p in new.submissions(n)]
                    new.print_func(menu[choice])
                else:
                    new.print_func(menu[choice], n)
                    new.print_func(menu[choice], n)
            elif choice[0] == "q":
                break
            else:
                 print "That is not a valid menu option."
    menu_loop()

if __name__ == "__main__":
    start_up()