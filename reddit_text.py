#!/usr/bin/env python

__author__ = 'tracyrohlin'

import random
from re import sub
from datetime import datetime
from collections import OrderedDict
from pprint import pprint
import os

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
            self.top_posts = self.subreddit.get_top_from_all
            response = raw_input("Would you like to save as text files? [y/n]\n").lower().strip()[0]
            if response[0].lower() == "y":
                self.save = True
                default_loc = "/Users/tracyrohlin/PycharmProjects/thesis_project/{}/".format(self.subreddit)
                self.loc = raw_input("Press ENTER to use default, otherwise enter location."
                                    "\nThe default location is: " + default_loc +"\n")
                if not self.loc:
                    self.loc = default_loc

        except Exception as error:
            print error
            print "Trouble connecting. Please try again."


    def try_unicode(self, text):
        new = []
        text = self.remove_unwanted(text)
        for word in text.split():
            try:
                new.append(word.encode("utf-8"))
            except:
                pass
        return self.token_and_tag(" ".join(new))


    def token_and_tag(self, text):
        try:
            tagged = nltk.pos_tag(nltk.word_tokenize(text))

            tog = []
            for item in tagged:
                word, tag = item
                tog.append("/".join([word, tag]))
            return " ".join(tog)
        except:
            print "Was unable to tag word due to unknown ASCII character."
            pass


    def remove_unwanted(self, text):
        text = sub(r"\\u000a", "", text) # removes usernames from text
        text = sub(r"\[deleted\]", "", text) # removes [deleted] from text
        text = sub("\[[\w+\s+]*\]\(.*\)", "", text) # removes links from text
        text = sub('"', '', text) # removes punctuation
        text = sub("'", '', text) # removes punctuation
        return text

    def submissions(self, n):
        """Grabs all the top posts from a subreddit."""

        min_score = 30
        assert n > 0, "The number of posts must be more than zero."
        res = []
        for submission in self.top_posts():
            if len(res) < n:
                if len(submission.selftext.lower()) >= self.min_length and submission.score >= min_score:
                        res.append((submission.title, submission))
            else:
                break
        if len(res) == 0:
            print "Sorry, r/{} appears to be image based.".format(self.subreddit)
            response = raw_input("Please provide another subreddit or press ENTER for a random subreddit.\n"
                                 ">> ").strip()
            self.get_subreddit(response)
        return res


    def save_submissions(self, text, iteration=None):
        """Labels file "1_subreddit_date", "2_subreddit_date", etc.
        to make it easier to distinguish separate posts from the same subreddit."""

        if iteration:
            file_name = "{}_{} - {}.txt".format(iteration, str(self.subreddit), str(datetime.now()))
        else:
            file_name = "{} - {}.txt".format(str(self.subreddit), str(datetime.now()))

        if not os.path.exists(self.loc):
            os.mkdir(self.loc)
        with open(os.path.join(self.loc, file_name), "wb") as file:
            print "Working..."
            file.write(text)
            print "Saved entry into a corpus file."


    def get_all_posts(self, n):
        """Grabs n posts from the subreddit and saves them as corpus files."""
        all_posts = [t for t in self.submissions(n)]

        post = ""
        i=1
        for p in all_posts:
            print "\nWorking on post #{}...".format(i)
            post_body = "Title: {0}\n{1}{2}".format(self.try_unicode(p[0]), self.try_unicode(p[-1].selftext.lower()), "\n"*2)
            post += post_body
            post += "="*30 +"\n\n"

            if self.save:
                self.save_submissions(post, i)
            i+=1
        return "\nRetrieved posts:\n\n" + post


    def get_all_comments(self, n):
        """Grabs comments from n posts and saves them as corpus files."""

        posts = [p[1] for p in self.submissions(n)]
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
                    total_comments += comment+ ("\n"*2)
                i+=1
            total_comments += "\n"+"+"*30 +"\n"

            if self.save:
                self.save_submissions(total_comments)

        return total_comments


    def combine_texts(self, n):
        """Combines posts and comments into one corpus file."""

        result = ""
        # the data has already been tagged so it must be split on the demarcator
        posts = self.get_all_posts(n).split("="*30)[:-1]
        comments = self.get_all_comments(n).split("+"*30)[:-1]
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
        if self.save:
            self.save_submissions(text)

        if score >=30:
                print "\n{} is a popular post.\n".format(title)

        if not text:
            print "Sorry, r/{} appears to be image based.\n".format(self.subreddit)
            response = raw_input("Please provide another subreddit or press ENTER for a random subreddit.\n"
                                 ">> ").strip()
            self.get_subreddit(response)
            self.get_random_post(n)
        else:
            return "\nRetrieved random post:\n\n" + text + "\n"


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
            res = "\nRetrieved random comment:\n\n"
            res += "Comment karma: {} \n\n{}".format(score, only_post) + "\n"
            return res

        except:
            print "No comments were found among new posts"


    def print_func(self, function, n):
        try:
            print function(n)
        except Exception as e:
            print e


def start_up():
    subreddit = raw_input("What subreddit would you like to grab posts from?"
                          "\nTo grab a random subreddit, press ENTER.\n>> ")
    new = RedditText()
    new.get_subreddit(subreddit)


    menu = OrderedDict([
        ("ga", new.combine_texts),
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
                try:
                    n = raw_input("How many posts would you like to grab?\n")
                    n = int(n)
                except Exception as e:
                    print e
                new.print_func(menu[choice], n)
            elif choice[0] == "q":
                break
                print "That is not a valid menu option."
    menu_loop()

if __name__ == "__main__":
    start_up()

#new = RedditText("xxfitness")
#print new.combine_texts(1)