import datetime
import json
import logging
import csv
import tweepy
import os

consumer_key = os.environ["TWITTER_KEY"]
consumer_secret = os.environ["TWITTER_SECRET"]
fieldnames = ['user_id', 'stat_id', 'creation', 'tweet_body', 'name']
csv_name = "data/tweets.csv"
file_exists = os.path.isfile(csv_name)


class StreamListener(tweepy.StreamListener):
    def __init__(self):
        super(StreamListener, self).__init__()
        self.exit = False

    def on_status(self, status):
        if status.lang == 'en' and 'RT'.upper() not in status.text:
            stat = status.text
            stat = stat.replace('\n', '')
            stat = stat.replace('\t', '')

            user_id = status.user.id_str
            stat_id = status.id_str
            create = str(status.created_at)
            name = status.user.screen_name
            # print("got tweet", stat)
            with open(csv_name, 'a') as ank:
                writer = csv.DictWriter(ank, fieldnames=fieldnames)
                print("writing row")
                writer.writerow({
                    "user_id": user_id,
                    "stat_id": stat_id,
                    "creation": create,
                    "tweet_body": stat,
                    "name": name
                })
                ank.close()
                print("done writing")

    def on_error(self, status_code):
        if status_code == 420:
            cdate = "Error code 420 at:" + str(datetime.datetime.now())
            logging.info(cdate)
            logging.info("Sleeping for 15 mins")
            self.exit = True


def write_header():
    with open(csv_name, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()  # file doesn't exist yet, write a header


def app():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.access_token = "1102697425884471297-o0RcQVuc8zDNtC6BUF4UzFeNe96N3L"
    auth.access_token_secret = "7cb1LkX1bWAkJujcPZqNzvIi0lLhwrMGGJZsX0sF59z0i"
    api = tweepy.API(auth)
    listener = StreamListener()
    # write the header to the cv if it doesnt have it already
    write_header()
    while not listener.exit:
        tweepy.Stream(api.auth, listener=listener).sample()
    print("exiting after hitting rate limit, has errored out")
    return 0


if __name__ == '__main__':
    app()
