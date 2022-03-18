def process_streams(tweets):
    # import nltk
    # nltk.download('stopwords')
    # Convert to json
    json_load_udf = udf(json_load, StringType())
    tweets = tweets.withColumn("json", json_load_udf("value"))

    # Get id
    get_tweet_field_udf = udf(get_tweet_field, StringType())
    tweets = tweets.withColumn("id", get_tweet_field_udf("value", lit('id')))

    # Get created_at
    get_tweet_field_udf = udf(get_tweet_field, StringType())
    tweets = tweets.withColumn("created_at", get_tweet_field_udf("value", lit('created_at')))

    # Get place full name
    get_tweet_field_udf = udf(get_tweet_field, StringType())
    tweets = tweets.withColumn("place_full_name", get_tweet_field_udf("value", lit('place/full_name')))

    # Get place country
    get_tweet_field_udf = udf(get_tweet_field, StringType())
    tweets = tweets.withColumn("place_country", get_tweet_field_udf("value", lit('place/country')))

    # Get place country code
    get_tweet_field_udf = udf(get_tweet_field, StringType())
    tweets = tweets.withColumn("place_country_code", get_tweet_field_udf("value", lit('place/country_code')))

    # Get place co-ordinates
    get_tweet_field_udf = udf(get_tweet_field, StringType())
    tweets = tweets.withColumn("place_coordinates", get_tweet_field_udf("value", lit('coordinates')))

    # Get place bounding_box co-ordinates
    get_tweet_field_udf = udf(get_tweet_field, StringType())
    tweets = tweets.withColumn("bounding_box_coordinates",
                               get_tweet_field_udf("value", lit('place/bounding_box/coordinates')))

    # Get place type
    get_tweet_field_udf = udf(get_tweet_field, StringType())
    tweets = tweets.withColumn("place_type", get_tweet_field_udf("value", lit('place/place_type')))

    # Get message
    get_message_udf = udf(get_message, StringType())
    tweets = tweets.withColumn("message", get_message_udf("value"))

    # Get cleaned words from message for analysis
    tweets = tweets.withColumn('words', tweets.message)
    # Remove HTML special entities (e.g. &amp;)
    tweets = tweets.withColumn('words', F.regexp_replace('words', r'\&\w*;', ''))
    # Convert @username to AT_USER
    tweets = tweets.withColumn('words', F.regexp_replace('words', '@[^\s]+', ''))
    # Remove tickers
    tweets = tweets.withColumn('words', F.regexp_replace('words', r'\$\w*', ' '))
    # Remove hyperlinks
    tweets = tweets.withColumn('words', F.regexp_replace('words', r'https?:\/\/.*\/\w*', ''))
    # Remove hashtags
    tweets = tweets.withColumn('words', F.regexp_replace('words', r'#\w*', ''))
    # Remove words with 2 or fewer letters
    # tweets = tweets.withColumn('words', F.regexp_replace('words', r'\b\w{1,2}\b', ''))
    # Remove whitespace (including new line characters)
    tweets = tweets.withColumn('words', F.regexp_replace('words', r'\s\s+', ' '))
    tweets = tweets.withColumn('words', F.regexp_replace('words', r'http\S+', ' '))
    # tweets = tweets.withColumn('words', F.regexp_replace('words', '@\w+', ' '))
    # tweets = tweets.withColumn('words', F.regexp_replace('words', '#', ' '))
    tweets = tweets.withColumn('words', F.regexp_replace('words', 'RT', ''))
    # tweets = tweets.withColumn('words', F.regexp_replace('words', ':', ' '))

    # my_udf = udf(lambda x: remove_stopwords(x), StringType())
    # tweets = tweets.withColumn('words',my_udf(tweets.words))

    # Drop unnesscessary data
    tweets = tweets.drop("value")
    tweets = tweets.drop("json")

    return tweets