import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt


class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self):
        
        consumerKey = 'VUYinmUXDCXFOpVCs6JaPwXVO'
        consumerSecret = 'F0SOaP00njdExQb8ufODVv2zIVAiQlBXm3Wcc2loVRHB00aol9'
        accessToken = '1038489334163243009-jhvAcrDcPAELkAgD0Ix7ahWvf1GdbL'
        accessTokenSecret = 'ayGiHFHGCVq70ozKVh0UsU5fscGdckdsJyvRxQFtDCcNs'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

       
        searchTerm = "Hrisheekesh4"
        NoOfTerms = 9

       
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)

        
        csvFile = open('result.csv', 'a')

        print("------------------------------------------------------------")
        csvWriter = csv.writer(csvFile)


        polarity = 0
        positive = 0
        negative = 0
        neutral = 0


        k=0
        for tweet in self.tweets:
            k=k+1
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            
            print(tweet.text)
            analysis = TextBlob(tweet.text)
           
            polarity += analysis.sentiment.polarity 
            flag=0
            if k!=9 and (analysis.sentiment.polarity == 0): 
                neutral += 1
            elif k!=9 and (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 1):
                positive += 1
            elif k!=9 and (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= 0):
                negative += 1
            elif k==9 and (analysis.sentiment.polarity == 0): 
                neutral += 2
                flag=1
            elif k==9 and (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 1):
                positive += 2
                flag=2
            elif k==9 and (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= 0):
                negative += 2
                flag=3
            if flag==1:
                neutral=neutral-(neutral-1)*(1/9)
                positive=positive-(positive)*(1/9)
                negative=negative-(negative)*(1/9)
            elif flag==2:
                positive=positive-(positive-1)*(1/9)
                neutral=neutral-(neutral)*(1/9)
                negative=negative-(negative)*(1/9)
                
            elif flag==3:
                negative=negative-(negative-1)*(1/9)
                positive=positive-(positive)*(1/9)
                neutral=neutral-(neutral)*(1/9)
                
     
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        positive = self.percentage(positive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)
       
        polarity = polarity / NoOfTerms

        print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
        print()
        print("General Report: ")

        if (polarity == 0):
            print("Neutral")
        elif (polarity > 0 and polarity <= 10):
            print("Positive")
        elif (polarity > -10 and polarity <= 0):
            print("Negative")

        print()
        print("Detailed Report: ")
        print(str(positive) + "% people thought it was positive")
        print(str(negative) + "% people thought it was negative")
        print(str(neutral) + "% people thought it was neutral")

        self.plotPieChart(positive, negative, neutral, searchTerm, NoOfTerms)


    def cleanTweet(self, tweet):
        
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

   
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, negative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]']
        sizes = [positive, neutral, negative]
        colors = ['green','blue','red']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How is ' + searchTerm + ' based on the analysis of his recent ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()



if __name__== "__main__":
    sa = SentimentAnalysis()
    sa.DownloadData()