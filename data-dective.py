import csv
import sys
import os
from pathlib import Path


def load_raw_data(filename):
    path = Path(filename)

    if not path.exists():
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    raw_tweets = []
    with path.open(mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            raw_tweets.append(row)

    return raw_tweets


def clean_data(tweets):
    # """
    # QUEST 1: Handle missing fields.
    # Check for missing text, and replace empty likes/retweets with 0.
    # Return a clean list of tweets.
    # """
    cleaned = []
    removed_missing_text = 0
    fixed_likes = 0
    fixed_retweets = 0
    for row in tweets:
        text_value = str(row.get("Text", "")).strip()
        if not text_value:
            removed_missing_text += 1
            continue
        likes_raw = str(row.get("Likes", "")).strip()
        retweets_raw = str(row.get("Retweets", "")).strip()

        try:
            likes = int(likes_raw)
        except ValueError:
            likes = 0
            fixed_likes += 1
        try:
            retweets = int(retweets_raw)
        except ValueError:
            retweets = 0
            fixed_retweets += 1

        cleaned_row = row.copy()
        cleaned_row["Text"] = text_value
        cleaned_row["Likes"] = likes
        cleaned_row["Retweets"] = retweets

        cleaned.append(cleaned_row)
    stats = {
        "removed_missing_text": removed_missing_text,
        "fixed_likes": fixed_likes,
        "fixed_retweets": fixed_retweets,
    }
    return cleaned, stats


def find_viral_tweet(tweets):
    # """
    # QUEST 2: Loop through the list to find the tweet with the highest 'Likes'.
    # Do not use the max() function.
    # """
    # pass
    if not tweets:
        return None
    best_tweet = tweets[0]
    try:
        best_likes = int(str(best_tweet.get("Likes", "")).strip())
    except ValueError:
        best_likes = 0

    for row in tweets:
        try:
            current_likes = int(str(row.get("Likes", "")).strip())
        except ValueError:
            current_likes = 0

        if current_likes > best_likes:
            best_likes = current_likes
            best_tweet = row

    return best_tweet


def custom_sort_by_likes(tweets):
    # by 'Likes' in descending order. NO .sort() allowed!
    # Selection Sort
    n = len(tweets)
    for i in range(n - 1):
        best_index = i

        for j in range(i + 1, n):
            try:
                j_likes = int(str(tweets[j].get("Likes", "")).strip())
            except ValueError:
                j_likes = 0

            try:
                best_likes = int(str(tweets[best_index].get("Likes", "")).strip())
            except ValueError:
                best_likes = 0

            if j_likes > best_likes:
                best_index = j

        tweets[i], tweets[best_index] = tweets[best_index], tweets[i]

    return tweets


def search_tweets(tweets, keyword):
    # """
    # QUEST 4: Search for a keyword and extract matching tweets into a new list.
    # """
    # pass
    matches = []
    keyword = str(keyword).strip().lower()

    if not keyword:
        return matches
    for row in tweets:
        text = str(row.get("Text", "")).lower()
        if keyword in text:
            matches.append(row)

    return matches


if __name__ == "__main__":
    # Load the messy data
    dataset = load_raw_data("twitter_dataset.csv")
    print(f"Loaded {len(dataset)} raw tweets.\n")

    # Fixed data
    clean_dataset, stats = clean_data(dataset)
    print("Rows removed (missing text):", stats["removed_missing_text"])
    print("Rows fixed (invalid/missing likes):", stats["fixed_likes"])
    print("Rows fixed (invalid/missing retweets):", stats["fixed_retweets"])

    # Search Keywords
    keyword = input("Enter Keyword to search: ")
    results = search_tweets(clean_dataset, keyword)
    print("Found", len(results), "matches")
    for i, tweet in enumerate(results, start=1):
        print(f"\n#{i}")
        print("Username", tweet.get("Username", "Unkown"))
        print("Likes", tweet.get("Likes", 0))
        print("Text", tweet.get("Text", ""))

    # Viral Tweet
    viral = find_viral_tweet(clean_dataset)
    if viral is not None:
        print("\n Most Engaging Tweet: ")
        print("Username:", viral.get("Username", "Unkwown"))
        print("Likes:", viral.get("Likes", 0))
        print("Text", viral.get("Text", ""))
    else:
        print("No tweets available")

    # Top 10 most liked tweets

    sorted_tweets = custom_sort_by_likes(clean_dataset)

    print("\n Top 10 Most Liked Tweets:")
    for i, tweet in enumerate(sorted_tweets[:10], start=1):
        print(f"\n#{i}")
        print("Username", tweet.get("Username", "Unkown"))
        print("Likes", tweet.get("Likes", 0))
        print("Text", tweet.get("Text", ""))

    # Call your functions here to complete the quests!
    # Example: clean_dataset = clean_data(dataset)
