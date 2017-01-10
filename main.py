import tweepy
import sys
from datetime import datetime, timedelta


def get_auths():
    try:
        secrets_file = open(sys.argv[1], 'r')
        return secrets_file.read().splitlines()
    except Exception as e:
        print(e)
        print("You have an issue with opening auth file "+sys.argv[1])
        print("Check the filepath and/or secret and key are in there" +
              " and try again")
        sys.exit(1)


def like_tweets(api, name):
    # gets all tweets from the past 24 hours on all armchair accounts
    yesterday = datetime.now() - timedelta(days=1)
    main_acc = api.user_timeline(screen_name=name)
    oldest = main_acc[-1].id - 1

    print("Liking statuses for "+name)
    i = 0
    while(main_acc[0].created_at > yesterday):
        for tweet in main_acc:
            try:
                api.create_favorite(tweet.id)
                i += 1
            except tweepy.TweepError:
                continue
        main_acc = api.user_timeline(screen_name=name,
                                     max_id=oldest)
        oldest = main_acc[-1].id - 1

    print("Liked "+str(i)+" statuses for "+name)


def get_usernames(read_file):
    try:
        names = open(read_file, 'r')
        return names.read().splitlines()
    except Exception as e:
        print(e)
        print("You have an issue with opening names file "+read_file)
        print("Check the filepath and try again")
        sys.exit(1)


def main():
    if len(sys.argv) != 3:
        print("Make sure to put in the auth and accounts filename")
        sys.exit(1)
    try:
        consumer_key, consumer_secret, access_token, token_secret = get_auths()
    except:
        print("There are not enough values in your secrets file. Try again")
        sys.exit(1)

    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, token_secret)
        api = tweepy.API(auth)
    except:
        print("There was a problem with the Twitter Authentication!")
        sys.exit(1)

    names = get_usernames(sys.argv[2])
    for account in names:
        like_tweets(api, account)

if __name__ == '__main__':
    main()
