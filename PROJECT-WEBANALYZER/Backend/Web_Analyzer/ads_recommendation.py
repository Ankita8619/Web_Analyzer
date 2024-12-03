from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
import spacy

# Load the spaCy model globally
nlp = spacy.load('en_core_web_sm')

def extract_keywords(text):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = X.sum(axis=0).A1
    tfidf_scores_dict = dict(zip(feature_names, tfidf_scores))
    keywords = [word for word, score in sorted(tfidf_scores_dict.items(), key=lambda x: x[1], reverse=True)[:50]]
    return keywords

def extract_entities(text):
    doc = nlp(text)
    entities = [entity.text.lower() for entity in doc.ents]
    return entities

def recommend_ads(text, ad_topic_mapping):
    # Extract keywords using TF-IDF
    keywords = extract_keywords(text)

    # Extract named entities using spaCy
    entities = extract_entities(text)

    # Generate ad topics
    ad_topics = set()
    for keyword in keywords:
        if keyword in ad_topic_mapping:
            ad_topics.add(ad_topic_mapping[keyword])
    for entity in entities:
        if entity in ad_topic_mapping:
            ad_topics.add(ad_topic_mapping[entity])

    return list(ad_topics)[:6]  # Return top 6 ad topics

def sentiment_analysis(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return {
        "polarity": sentiment.polarity,
        "subjectivity": sentiment.subjectivity,
        "overall_sentiment": "Positive" if sentiment.polarity > 0 else "Negative" if sentiment.polarity < 0 else "Neutral"
    }

def calculate_score(polarity, subjectivity, sentiment):
    # Normalize polarity to 0-100
    polarity_score = (polarity + 1) * 50  # Converts -1 to 1 into 0 to 100

    # Normalize subjectivity to 0-100
    subjectivity_score = subjectivity * 100

    # Initial weighted score: 50% polarity + 30% subjectivity
    score = (0.5 * polarity_score) + (0.3 * subjectivity_score)

    # Sentiment adjustment: +10 for Positive, -10 for Negative, no change for Neutral
    if sentiment == "Positive":
        score += 10
    elif sentiment == "Negative":
        score -= 10

    # Ensure the score is within 0-100
    return max(0, min(100, round(score)))

def generate_text_report(text, ad_topic_mapping):
    # Extract sentiment
    sentiment = sentiment_analysis(text)

    # Recommend ads
    ad_topics = recommend_ads(text, ad_topic_mapping)
    
    
    total_score = calculate_score(sentiment["polarity"], sentiment["subjectivity"], sentiment["overall_sentiment"])

    # Generate numerical data
    numerical_data = {
        "polarity_score": {
            "title": "Polarity Score",
            "value": round(sentiment["polarity"], 2),
            "details": "The sentiment polarity score (-1 to 1)."
        },
        "subjectivity_score": {
            "title": "Subjectivity Score",
            "value": round(sentiment["subjectivity"], 2),
            "details": "The subjectivity score (0 to 1)."
        },
        "total_keywords": {
            "title": "Total Keywords Extracted",
            "value": len(extract_keywords(text)),
            "details": "Number of keywords extracted using TF-IDF."
        },
        "total_entities": {
            "title": "Total Named Entities Extracted",
            "value": len(extract_entities(text)),
            "details": "Number of named entities identified using spaCy."
        },
        "positive_sentiment": {
            "title": "Positive Sentiment",
            "value": 1 if sentiment["overall_sentiment"] == "Positive" else 0,
            "details": "Whether the overall sentiment is positive (1 for Yes, 0 for No)."
        },
        "negative_sentiment": {
            "title": "Negative Sentiment",
            "value": 1 if sentiment["overall_sentiment"] == "Negative" else 0,
            "details": "Whether the overall sentiment is negative (1 for Yes, 0 for No)."
        },
        "neutral_sentiment": {
            "title": "Neutral Sentiment",
            "value": 1 if sentiment["overall_sentiment"] == "Neutral" else 0,
            "details": "Whether the overall sentiment is neutral (1 for Yes, 0 for No)."
        },
        "top_ads_recommended": {
            "title": "Total Recommended Ads",
            "value": len(ad_topics),
            "details": "Number of ad topics recommended based on the analysis."
        }
    }

    # Enhanced One-Liner Details (Top 6 Ad Topics)
    one_liner_data = [
        {"title": f"Top Ad Topic {i+1}", "details": f"Recommended Ad Topic: {ad_topics[i]}"} 
        for i in range(len(ad_topics))
    ]

    # Final Report
    return {
        "numerical_data": numerical_data,
        "one_liner_data": one_liner_data,
        "total_score": total_score
    }
