# RedditCorpus
Creates a corpus of text files from specific subreddits.

The user can provide a subreddit or one can be chosen randomly by the PRAW module.  The program then grabs a specific number of top posts in that subreddit.

This is an example of the program:

    What subreddit would you like to grab posts from?
    To grab a random subreddit, press ENTER.
    >> 
    Current subreddit is CyanideandHappiness

    Would you like to save as text files? [y/n]
    >>n
    Enter 'q' to quit.
    [ga] Combines posts and comments into one corpus file.
    [ap] Grabs n posts from the subreddit and saves them as corpus files.
    [ac] Grabs comments from n posts and saves them as corpus files.
    [rp] Grabs a random post from the top n posts in the same subreddit.
    [rc] Grabs a random comment from the same subreddit.
    Action:  ga
    How many posts would you like to grab?
    2

If the subreddit is image based, it will ask the user to provide another subreddit:
  
    2
    Sorry, r/CyanideandHappiness appears to be image based.
    Please provide another subreddit or press ENTER for a random subreddit.
    >> xxfitness
    Current subreddit is xxfitness
    
Then the menu shows up with several options.
    
    Enter 'q' to quit.
    [cp] Combines posts and comments into one corpus file.
    [ap] Grabs n posts from the subreddit and saves them as corpus files.
    [ac] Grabs comments from n posts and saves them as corpus files.
    [rp] Grabs a random post from the top n posts in the same subreddit.
    [rc] Grabs a random comment from the same subreddit.
    Action:  ac
    
    Working on comment #1...

    Working on comment #2...

    Working on comment #3...
    
    ...
    
    Working on comment #156...
    Working...
    Saved entry into a corpus file.
    
The corpus file is tagged using the NLTK tagger, stemmed and has stop words removed.  It is then saved as a corpus file:

    Title: idea wrong two seconds giving skinnyfat nsfw
    Karma: 6
    Date: 1432356504.0
    long story short skinny fat think weigh lbs working past two months seen zero improvements seriously starting bring record eat calories less weekdays consisting chicken breast seasoned something lean ground beef cauliflower mash spinach broccoli carrots flax whole grain pita bread eating week deli turkeychicken greek yogurt apples eat around calories per day weekend usually burger fries piece
    
    New comment:
    Karma: 1
    wasnt judgemental completely misjudge tone actually try nice surprise reply never claim special snowflake ive really bad compare others

    New comment:
    Karma: 5
    promptly escort premise 


    ++++++++++++++++++++++++++++++


The get_random_comment() function grabs a number of new posts (as opposed to top posts) and randomly selects and returns one:

    Retrieved random comment:
    Karma: 1 

    design intermittent fasting set equal intake workout rest days 

get_random_post() does the same.  combine_texts() saves all the comments and the post itself as one large corpus file.

Karma_Graph.py creates a simple histogram with the Karma scores from each post/comment as the value:

![Example of the Karma graph.](https://github.com/TracyMRohlin/RedditCorpus/blob/master/fitness/RedditCorpus%20Karma%20Scores.png)

Naive_Bayes_model.py creates a multinomial Naive Bayes classifier that classifies reddit posts that have scores 2 standard deviations above the gathered mean as "popular"

    >> ./popularity_cutoff.py /Users/user/PycharmProjects/RedditCorpus/xxfitness
    22.0
    
To create a general NB classifier based on a bag of words model on the validation dataset ("t" for testing data):

    >>./Naive_Bayes_model.py /Users/tracyrohlin/PycharmProjects/RedditCorpus/xxfitness/ bow v
    Classifying the initial data.
    Creating the data frame.
    Classifying the validation data.
    Creating the data frame.
    Total documents classified: 2001
    Score: 0.741312741313
    Confusion matrix:
    [[192  63]
    [ 71 174]]

To create a NB classifier based on the LDA model, the user has to provide the number of topics that the model should calculate probablities for:

    >> ../Naive_Bayes_model.py /Users/tracyrohlin/PycharmProjects/RedditCorpus/xxfitness/ lda v --num_topics 20
    ...
    Total documents classified: 2001
    Score: 0.639316239316
    Confusion matrix:
    [[187  68]
    [143 102]]

For an SVM using TFIDF scores:

    ./SVM_model.py /Users/tracyrohlin/PycharmProjects/RedditCorpus/xxfitness/ tfidf v
    ...
    Total documents classified: 2001
    Score: 0.771126760563
    Confusion matrix:
    [[219  36]
    [ 94 151]]

(Note, the regularization parameters can highly affect the accuracy of the SVM so users should play around with it to see what works best).
