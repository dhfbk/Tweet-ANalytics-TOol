import json_lines
import json
import pandas as pd
import time
import datetime
filename = '2021-06-30_04-01_donn_nomadonna.jsonl'
df1 = pd.DataFrame(columns =["id",
                                "user_id",
                                "to_userid",
                                "to_tweetid",
                                "retweeted_id",
                                "retweeted_user_id",
                                'user_screen_name',
                                "mentioned_ids",
                                "mentioned_names",
                                "timestamp_utc",
                                "matching_rules",
                                "lang",
                                "reply_count",
                                "like_count",
                                "text",
                                "retweeted_user",
                                "followers_count",
                                "textLemm",
                                "collected_via",
                                "quoted_id","retweet_count","user_friends","user_followers",'hashtags'])
df = pd.DataFrame(columns =["id",
                                "user_id",
                                "to_userid",
                                "to_tweetid",
                                "retweeted_id",
                                "retweeted_user_id",
                                'user_screen_name',
                                "mentioned_ids",
                                "mentioned_names",
                                "timestamp_utc",                                
                                "matching_rules",
                                "lang",
                                "reply_count",
                                "like_count",
                                "text",
                                "retweeted_user",
                                "followers_count",
                                "textLemm",
                                "collected_via","quoted_id","retweet_count","user_friends","user_followers","hashtags"])

with open('./data/my_filename.jsonl', 'r') as json_file:
    json_list = list(json_file)
index = 0
try:
for json_str in json_list:
    tweet = json.loads(json_str)
    no = 0
    mytime = int(time.mktime(datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y').timetuple()))
    myhtg=' |+ '
    try:
      for k in range(len(tweet['entities']['hashtags'])):
        myhtg = tweet['entities']['hashtags'][k]['text'].replace('#','')+' | '+ myhtg
    except:
      pass 
    myhtg = myhtg.replace('|  |+','')
    myhtg = myhtg.replace('|+','')    
    try:
      df1 = pd.DataFrame({"index": '1',"user_friends":tweet['user']['friends_count'],"user_followers":tweet['user']['followers_count'], "collected_via":'twitterexplorer','user_screen_name':tweet['user']['screen_name'],"timestamp_utc":mytime,"lang":tweet['lang'],"id":tweet['id_str'],"matching_rules":tweet["matching_rules"], "retweeted_id":tweet['retweeted_status']['id_str'],"retweet_count":tweet["retweet_count"],"like_count":tweet['like_count'],"follower_count":tweet['user']['followers_count'],"user_id":tweet['user']['id_str'],"retweeted_user_id":tweet['retweeted_status']['user']['id_str'],'text':tweet['text'].replace('user','').replace('url','').replace('number',''),'textLemm':tweet['text'].replace('user','').replace('url','').replace('number',''),"retweeted_user":tweet['retweeted_status']['user']['screen_name'],'hashtags':myhtg.replace(' ','')})
    except:
      break
      try:
        df1 = pd.DataFrame({"index": '1',"user_friends":tweet['user']['friends_count'],"user_followers":tweet['user']['followers_count'], "collected_via":'twitterexplorer','user_screen_name':tweet['user']['screen_name'],"timestamp_utc":mytime,"lang":tweet['lang'],"id":tweet['id_str'],"matching_rules":tweet["matching_rules"], "retweet_count":tweet["retweet_count"],"like_count":tweet['like_count'],"follower_count":tweet['user']['followers_count'],"user_id":tweet['user']['id_str'],'text':tweet['text'].replace('user','').replace('url','').replace('number',''),'textLemm':tweet['text'].replace('user','').replace('url','').replace('number',''),'hashtags':myhtg.replace(' ','')})
        print(ciao)
      except:
        no=1
        pass      
      if no ==0:
  #      print(df.columns)
  #      print(df1.columns)
        #df =  pd.concat([df1,df.loc[:]])
        df = df.append(df1,ignore_index = True)
        index = index +1
        print(str(index))
        #if index > 2000:
        #   df.to_csv('smallfile_16_it_all.csv')
        #  break

except:
  df.to_csv('2021-06-30_04-01_donn_nomadonna.csv')
df.to_csv('2021-06-30_04-01_donn_nomadonna.csv')  
