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

It then asks whether the user would like to save the text files and whether to save the untaggable words in a log file.   Untaggable words often occur do to unicode errors.

    Would you like to save as text files? [y/n]
    >>y
    Press ENTER to use default, otherwise enter location.
    The default location is: /Users/girllunarexplorer/PycharmProjects/xxfitness/
    Would you like to log all the untagged words? [y/n]
    >>y
    
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

    ...
    New comment:
    Karma: 1
    response/NN necessarily/RB uncalled/VBD take/VBD much/RB get/NN acknowledge/NN hypocrisy./NNP seem/NN lack/VBG     self-awareness./NNP say/VBP something/NN like/IN saddens/NNS take/VBD look/NN history/NN apologise,/NN come/NNS across/IN quite/RB judgemental,/NN although/IN could/MD easily/RB word/VBD differently/RB tried./NNP yet/RB youre/NN surprise/VBD would/MD reply/RB similar/JJ manner./NNP think/NN suck/NNS youve/NN rough/IN go/IN aspect/NNS life,/NN dont/NN wish/NN upon/IN anyone,/NN youre/NN special/JJ snowflake./NNP cant/NN come/NN across/IN judgmental/JJ towards/NNS others/NNS expect/NN treat/NN differently./NNP
    
    New comment:
    Karma: 1
    wasnt/NN judgemental./NNP completely/RB misjudge/VBD tone./NNP actually/RB try/VBG nice,/NN surprise/VBD reply./NNP     never/RB claim/NN special/JJ snowflake/NN ive/JJ really/RB bad/JJ compare/VBN others./NNP

    New comment:
    Karma: 5
    promptly/RB escort/VBD premise/NN


    ++++++++++++++++++++++++++++++


The get_random_comment() function grabs a number of new posts (as opposed to top posts) and randomly selects and returns one:

    Retrieved random comment:
    Karma: 1 

    http://www.1percentedge.com/ifcalc//NN design/VBN intermittent/NN fasting,/NN set/NN equal/JJ intake/NN workout/IN rest/NN     days./NNP

get_random_post() does the same.  combine_texts() saves all the comments and the post itself as one large corpus file.

Karma_Graph.py creates a simple histogram with the Karma scores from each post/comment as the value:

![Example of the Karma graph.](https://github.com/TracyMRohlin/RedditCorpus/blob/master/fitness/RedditCorpus%20Karma%20Scores.png)

Naive_Bayes_model.py creates a multinomial Naive Bayes classifier that classifies reddit posts that have scores 2 standard deviations above the gathered mean as "popular"

    >> ./popularity_cutoff.py /Users/user/PycharmProjects/RedditCorpus/fitness
    11.0
          
    >>./remove_outliers.py /Users/tracyrohlin/PycharmProjects/RedditCorpus/fitness
    A total of 43 outliers were removed from the corpus
    
To create a general NB classifier based on a bag of words model:

    >>./Naive_Bayes_model.py /Users/tracyrohlin/PycharmProjects/RedditCorpus/fitness bow
    Total documents classified: 904
    Score: 0.567455911369
    Confusion matrix:
    [[ 44  34]
    [ 33 793]]

To create a NB classifier based on the LDA model, the user has to provide the number of topics that the model should calculate probablities for, as well as the number per words that each topic should be associated with:

    >> ./Naive_Bayes_model.py /Users/tracyrohlin/PycharmProjects/RedditCorpus/fitness lda --num_topics 20 --num_words 20
    Total documents classified: 904
    Score: 0.483461448689
    Confusion matrix:
    [[ 35  43]
    [ 34 792]]
    
    


    
