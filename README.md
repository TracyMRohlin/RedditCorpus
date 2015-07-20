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
    >> yoga
    Current subreddit is yoga
    Would you like to save as text files? [y/n]
    >>y
    Press ENTER to use default, otherwise enter location.
    The default location is: /Users/girllunarexplorer/PycharmProjects/yoga/
    
    Working on comment #1...

    Working on comment #2...

    Working on comment #3...
    
    ...
    
    Working on comment #156...
    Working...
    Saved entry into a corpus file.
    
The corpus file is tagged using the NLTK tagger and saved as a corpus file:

    Title: So/IN I/PRP just/RB designed/VBN some/DT yoga/NN mats/NNS for/IN dudes/NNS
    i/PRP never/RB thought/VBD id/VBN get/NN into/IN yoga/NN ,/, but/CC when/WRB i/PRP threw/VBP out/RP my/PRP$ back/NN a/DT couple/NN of/IN years/NNS ago/IN i/PRP got/VBD really/RB into/IN it/PRP ./. but/CC i/PRP felt/VBD kind/JJ of/IN weird/JJ as/IN a/DT dude/NN ,/, carrying/VBG my/PRP$ girlfriends/NNS hot/JJ pink/NN yoga/NN mat/NN to/TO work/VB ./. so/RB i/PRP joked/VBD that/IN i/PRP should/MD make/VB some/DT mats/NNS that/WDT looked/VBD like/IN badass/NN things/NNS on/IN your/PRP$ back/NN when/WRB you/PRP walked/VBD around/IN town/NN ./. my/PRP$ friends/NNS thought/VBD it/PRP was/VBD funny/JJ and/CC i/PRP should/MD do/VB it/PRP ,/, so/RB i/PRP came/VBD up/RP with/IN a/DT few/JJ designs/NNS like/IN a/DT quiver/NN of/IN arrows/NNS and/CC a/DT giant/JJ burrito/NN on/IN your/PRP$ back/NN ./. i/PRP made/VBD a/DT small/JJ run/NN of/IN them/PRP and/CC id/VBD like/IN to/TO see/VB if/IN theyre/NN actually/RB awesome/VB and/CC worth/NN pursuing/VBG ./. please/NN check/NN them/PRP out/RP :/: [/: brogamats.com/JJ ]/NN (/: http/NN :/: //brogamats.com/JJ )/NN ./. thanks/NNS so/RB much/RB ,/, ~dan/JJ

    Comments from post:
    First/NNP off/IN ,/, I/PRP love/VBP the/DT concept/NN ./. I/PRP would/MD buy/VB in/IN for/IN the/DT humor/NN ./. I/PRP ,/, being/VBG a/DT larger/JJR guy/NN ,/, do/VBP not/RB find/VB the/DT standard/JJ yoga/NN mat/NN size/NN to/TO be/VB large/JJ enough/RB ./. I/PRP would/MD imagine/VB more/RBR of/IN the/DT dude/NN market/NN to/TO agree/VB ./.

The get_random_comment() function grabs a number of new posts (as opposed to top posts) and randomly selects and returns one:

    Retrieved random comment:

    Comment karma: 1 

    I/PRP dont/VBP wear/JJ a/DT headband/NN ,/, but/CC its/PRP$ worth/NN a/DT shot/NN ./. Ive/NNP never/RB worn/VB one/CD because/IN I/PRP figured/VBD I/PRP did/VBD enough/RB wiping/VBG without/IN it/PRP ./. Ill/NNP try/NN though/IN ,/, thanks/NNS !/.

get_random_post() does the same.
