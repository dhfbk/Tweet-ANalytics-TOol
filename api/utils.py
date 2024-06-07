import datetime as dt
import pandas as pd
import numpy as np 
import json
from wordcloud import WordCloud
import base64
import io
import re

from twitterexplorer.communitydetection import *
from twitterexplorer.d3networks import *
from twitterexplorer.networks import *

import matplotlib.pyplot as plt
import altair as alt
# from altair_saver import save

def load_data(dataset):
    df = pd.read_csv(dataset,
                     dtype={"id":str,
                            "user_id":str,
                            "to_userid":str,
                            "to_tweetid":str,
                            "retweeted_id":str,
                            "retweeted_user_id":str,
                            "quoted_id":str,
                            "quoted_user_id":str,
                            "mentioned_ids":str,
                            "mentioned_names":str,
                            "hashtags":str
                            },
                    low_memory=False,
                 )
    df['timestamp_utc'].astype('int')
    df = df.drop_duplicates('id')
    return df   


def find_out_tweet_type(row):
    if type(row['retweeted_id']) == str:
        return 'retweet'
    if type(row['quoted_id']) == str:
        return 'quote'
    if type(row['to_userid']) == str:
        return 'reply'
    else:
        return 'regulartweet'


def groupby_type(df, myfreq = '1H'):
    dfc = df.copy()
    dfc['type'] = dfc.apply(lambda row: find_out_tweet_type(row), axis=1)
    dfc['ts_dt'] = pd.to_datetime(dfc['timestamp_utc'], unit= 's')    
    dfc = dfc.set_index("ts_dt")
    grouper = dfc.groupby([pd.Grouper(freq=myfreq), 'type'])
    result = grouper['type'].count().unstack('type').fillna(0)
    existing_tweettypes = list(result.columns)
    result['total'] = 0
    for tweettype in existing_tweettypes:
        result['total'] += result[tweettype]
    result["datetime"] = result.index
    return result 


def count_tweets(grouped):
    types = list(grouped.columns)[:-2]
    counts = dict()
    for t in types:
        counts[t] = int(grouped[t].sum())
    tot = 0
    for k in counts:
        tot = tot + counts[k]    
    counts['total'] = int(tot)
    return(counts)

def date_to_datetime(d):
    return dt.datetime(d.year,d.month,d.day)



def date_to_ts(dataset, time, input_d):
# se data è None, in prima istanza prova a leggere le date di inizio/fine del dataset. 
# Altrimenti prende il giorno corrente per il punto di fine e un anno prima per il punto di iinizio
    if input_d == None:
        if time == 'start':
            try:
                d = dt.date.fromisoformat(dataset['date_start'])
            except:                
                d = dt.date.today() + dt.timedelta(days=-3650)
        else:
            try:
                d = dt.date.fromisoformat(dataset['date_end'])
            except:                
                d = dt.date.today()
    else:
        try:
            if time == 'end':
                d = dt.date.fromisoformat(input_d) + dt.timedelta(days=1)
            else:
                d = dt.date.fromisoformat(input_d)
        except:
            if time == 'end':
                d = dt.date.today()
            else:
                d = dt.date.today() + dt.timedelta(days=-3650)
    return(int(date_to_datetime(d).timestamp()))

def select_timerange(df, ts0, ts1):
    df_tr = df[(df['timestamp_utc'] >= ts0) & (df['timestamp_utc']<= ts1)]   
    return df_tr


def custom_word_selection(df, word):
    selection = df[df['text'].str.contains(word, na=False)]
    return(selection)


def get_rtnet(df, dataset_info, d0 = None, d1 = None, words = None):
    df = get_custom_df(df, dataset_info, d0, d1, words)
    dataset_name = dataset_info['name']

    try:
        df = df.rename(columns = {'follower_count': 'user_followers'})
    except:
        pass

    interaction_type = 'retweet'
    rtn_giantcomponent = 1 
    privacy = 1
    rtn_aggregation_soft = 0
    rtn_aggregation_hard = 1
    aggregationmethod = 'soft'
    aggregationmethod = 'hard'
    rtn_louvain = True

    G = twitter_df_to_interactionnetwork(df=df, starttime = None, endtime = None,
                                            interaction_type=interaction_type)

    hard_aggregation_threshold = 2

    G = reduce_network(G,
                        giant_component=1,
                        aggregation=aggregationmethod,
                        hard_agg_threshold=hard_aggregation_threshold)

    G, cgl = compute_louvain(G)        
    RTN = d3_rtn(G,private = 1)
    RTN['graph'] = {}
    RTN['graph']['type'] = f"{interaction_type.capitalize()} network"
    RTN['graph']['N_nodes'] = len(RTN["nodes"])
    RTN['graph']['N_links'] = len(RTN["links"])
    RTN['graph']['keyword'] = 'tmp'
    RTN['graph']['collected_on'] = 'collectedon'
    RTN['graph']['first_tweet'] = 'firstdate_str'
    RTN['graph']['last_tweet'] = 'lastdate_str'

    x = rtn_html(data=RTN)
    return x


def get_htnet(df, dataset_info, d0 = None, d1 = None, words = None):
    custom_df = get_custom_df(df, dataset_info, d0, d1, words)
    dataset_name = dataset_info['name']

    try:
        custom_df = custom_df.rename(columns = {'follower_count': 'user_followers'})
    except:
        pass

    privacy = 1
    htn_giantcomponent = 1
    
    # new Elisa: adjust parameter based on the size of the dataset
    # node_thresh_htn = 3
    if len(custom_df) > 90000:
        node_thresh_htn = round(len(custom_df) / (len(custom_df) / 5))
    elif len(custom_df) < 90000 and len(custom_df) > 70000:
        node_thresh_htn = round(len(custom_df) / (len(custom_df) / 4))
    elif len(custom_df) < 70000 and len(custom_df) > 50000:
        node_thresh_htn = round(len(custom_df) / (len(custom_df) / 3))
    else:
        node_thresh_htn = 2
    # end Elisa
    
    link_thresh_htn = 1
    htn_louvain = 1

    H = twitter_df_to_hashtagnetwork(df = custom_df, starttime = None, endtime = None)

    H = reduce_semanticnetwork(H, giant_component=htn_giantcomponent, node_threshold=node_thresh_htn, link_threshold=link_thresh_htn)

    if len(H.get_diameter()) == 0:
        return None

    H, Hcg = compute_louvain(H)

    edgeslist = list(H.es)
    if len(edgeslist) <= 1:
        return None

    firstdate_str = str(dt.datetime.fromtimestamp(edgeslist[-1]["time"]))
    lastdate_str = str(dt.datetime.fromtimestamp(edgeslist[0]["time"]))

    HTN = d3_htn(H)
    HTN['graph'] = {}
    HTN['graph']['type'] = "Hashtag network"
    HTN['graph']['N_nodes'] = len(HTN["nodes"])
    HTN['graph']['N_links'] = len(HTN["links"])
    HTN['graph']['keyword'] = dataset_name
    HTN['graph']['collected_on'] = 'collectedon'
    HTN['graph']['first_tweet'] = 'firstdate_str'
    HTN['graph']['last_tweet'] = 'lastdate_str'
    HTN['version_number'] = 'version_number'

    x = htn_html(data=HTN)
    return x


def plot_tweetcounts(grouped_tweetdf):
    # get the right order for color plotting
    types = list(grouped_tweetdf.columns)[:-2]

    # counts = []
    # for t in types:
    #     counts.append(grouped_tweetdf[t].sum())
    # order_idx = np.array(counts).argsort()[::-1]
    # order = [types[i] for i in order_idx]
    
    counts = []
    order = ['regulartweet', 'retweet',  'quote','reply']
    for t in order:
        try:
            counts.append(grouped_tweetdf[t].sum())
        except:
            counts.append(0)
    # set color range
    domain = order.copy()
    domain.append('total')
    #range_ = ['#005AB5','#DC3220','#009E73','#ff7f0e','grey']
    range_ = ['#ff0000','#009fff','#009E73','#ff7f0e','grey']
    # plot 
    C1 = alt.Chart(grouped_tweetdf).mark_area(opacity=0.6).transform_fold(
        fold=order,
        as_=['variable', 'value']
    ).encode(
        alt.X('datetime:T', timeUnit='yearmonthdatehours', title="date"),
        alt.Y('value:Q', stack=None, title="tweet count"),
        color=alt.Color("variable:N",
                        legend=alt.Legend(title="tweet type"),
                        scale=alt.Scale(domain=domain, range=range_),
                         )
    )
    # plot total in background    
    C2 = alt.Chart(grouped_tweetdf).mark_area(opacity=0.15).encode(
        alt.X(f'datetime:T', timeUnit='yearmonthdatehours', title='date'),
        alt.Y('total:Q'),
        color=alt.value("black"),
        tooltip=['datetime:T', 'regulartweet', 'retweet', 'total'])
    return ((C1+C2).configure_axis(
        labelFontSize=12,
        titleFontSize=12,
    ).configure_legend(titleFontSize=12,labelFontSize=12),order,counts)


def get_custom_df(df, dataset_info, d0 = None, d1 = None, words = None):
    ts0 = date_to_ts(dataset_info,  'start', d0)
    ts1 = date_to_ts(dataset_info, 'end', d1)
    if ts0 > ts1: # controllo da inserire se data iniziale successiva a data finale. al momento metto ts1 come "today" 
        ts1 = date_to_ts(dataset_info, 'end', None)
    df_func = select_timerange(df, ts0, ts1)    

    # se in input c'è una stringa, seleziona solo i dati che contengono nel testo quella stringa
    if words:
        df_func = custom_word_selection(df_func, words)
    return df_func

def plot_dataset(df, dataset_info, d0 = None, d1 = None, words = None):
    custom_df = get_custom_df(df, dataset_info, d0, d1, words)

    myfreq = '1W'
    grouped = groupby_type(custom_df, myfreq)
    tweet_count_chart, order, counts = plot_tweetcounts(grouped)

    try:
        ret = tweet_count_chart.to_dict()
    except:
        return None

    ret['config']['view'] = {}
    ret['width'] = "container"
    return ret


def count_freq(df):
    myfreq = list()    
    for sentence in df['text']:
        tmpDict = {}
        for text in sentence.split(" "):
            if re.match(r"^(a|the|an|the|to|in|for|of|or|by|with|is|on|that|be)$", text):
                continue
            val = tmpDict.get(text, 0)
            tmpDict[text.lower()] = val + 1
        try:
            del tmpDict['']
        except:
            pass
        myfreq.append(tmpDict)
    df['freq'] = myfreq
    return (df)


# def generate_wordcloud(df):
#     myDict = dict()
#     for tmpDict in df['freq']:
#         for key in tmpDict:
#             try:
#                 myDict[key] = myDict[tmpDict[key]] + myDict[key]
#             except:
#                 myDict[key] = tmpDict[key]
#     wordcloud = WordCloud(width=900,height=500, max_words=1628,relative_scaling=1,normalize_plurals=False).generate_from_frequencies(myDict)
#     return(wordcloud)


def generate_wordcloud(df):
    myDict = dict()    
    for sentence in df['text']:
        sentence = str(sentence)
        tmpDict = {}
        sentence = sentence.replace("'",' ').replace(":",' ').replace(".",' ').replace(",",' ').replace('twitterexplorer',' ')
        sentence = sentence.replace("  "," ")
        for text in sentence.split(" "):
            if len(text) < 3:
                continue
            val = tmpDict.get(text, 0)
            tmpDict[text.lower()] = val + 1
            try:
                myDict[text.lower()] = myDict[text.lower()] + tmpDict[text.lower()]
            except:
                myDict[text.lower()] = tmpDict[text.lower()]
    wordcloud = WordCloud(width = 800, height = 400,
                    background_color ='white',min_font_size = 10).generate_from_frequencies(myDict)
    return(wordcloud)


def get_wc(df, dataset_info, d0 = None, d1 = None, words = None):
    df = get_custom_df(df, dataset_info, d0, d1, words)

    # df = count_freq(df)
    wordcloud = generate_wordcloud(df)
    output = io.BytesIO()
    wordcloud.to_image().save(output, format='PNG')
    return output.getvalue()
