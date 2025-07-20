import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Create the sentiment analyzer once for the whole file
vader = SentimentIntensityAnalyzer()

def analyze_sentiment(company_name: str, api_key: str):

    if not company_name or not api_key:
        return None, []

    # Setup the NewsAPI request URL
    url = (
        'https://newsapi.org/v2/everything'
        f'?q="{company_name}"&language=en&sortBy=publishedAt&apiKey={api_key}'
    )

    try:
        # Fetch news
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return "Could not fetch news.", []

        data = response.json()
        articles = data.get("articles", [])
        if not articles:
            return "Neutral (No articles found)", []

        # Get sentiment scores for the top 10 headlines with a title
        scores = []
        for article in articles[:10]:
            title = article.get("title")
            if title:
                score = vader.polarity_scores(title)["compound"]
                scores.append(score)

        if not scores:
            return "Neutral  (No valid headlines)", []

        # Calculate average sentiment
        avg = sum(scores) / len(scores)

        # Assign label
        if avg >= 0.05:
            label = f"Positive  ({avg:.2f})"
        elif avg <= -0.05:
            label = f"Negative  ({avg:.2f})"
        else:
            label = f"Neutral ({avg:.2f})"

        # Return the label and top 5 articles
        return label, articles[:5]

    except Exception as e:
        # Any kind of error — just print for debugging and return
        print(f"Error in analyze_sentiment: {e}")
        return "Could not connect to news service.", []
