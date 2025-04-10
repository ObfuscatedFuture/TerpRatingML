import requests
import pandas as pd
import json
from textblob import TextBlob

def main():
    def fetch_professor_data(professor_name):
        url = f"https://api.planetterp.com/v1/professor?name={professor_name}&reviews=true"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to fetch data. Status code: {response.status_code}"}

    professor_name = "Maksym Morawski"  # Replace with the desired professor's name

    test_professors = {
        1: "Maksym Morawski",
        2: "Shane Walsh",
        3: "Leigh Soares",
        4: "Susan Pramschufer",
        5: "Asim Ali",
        6: "Becky Epanchin-Niell",
        7: "Billie Ray",
        8: "James Hunt",
        9: "Melissa Hayes-Gehrke",
        10: "Leslie Pick",
        11: "Jacob Coutts",
        12: "Bailey Kier",
        13: "Humberto Coronado",
        14: "Daniel Sidman",
        15: "Justine DeCamillis",
        16: "Sarah Kilmer",
        17: "Andre Tits",
        18: "Cynthia Kershaw",
        19: "Ebonie Johnson Cooper",
        20: "Emily Dobson",
        21: "Martha Nell Smith",
        22: "Joseph Falvo",
        23: "Madeline Hsu",
        24: "Antoine Borrut",
        25: "Michel Cukier"
    }
    
    def calc_sentiment(text):
        analysis = TextBlob(text)
        return analysis.sentiment.polarity
    
    df = pd.DataFrame()

    # for professor_name in test_professors.items():
    #     professor_data = fetch_professor_data(professor_name)
    #     if "reviews" in professor_data:
    #         professor_reviews = pd.DataFrame(professor_data["reviews"])
    #         df = pd.concat([df, professor_reviews], ignore_index=True)

    # df.to_csv("test_professor_reviews.csv", index=False)
    # print("test data saved")

    df = pd.read_csv("all_professors_reviews.csv")
    # Drops rating for training

    df_no_rating = df.drop("rating", axis=1)

    # Adds sentiment column
    df['sentiment'] = df['review'].apply(calc_sentiment)
    # Adds columns with just the length of each review (maybe length is correlated with a good/bad review??)
    df['r_length'] = df['review'].apply(len)
    
    df.to_csv("processed_professor_reviews.csv", index=False)

    print(df_no_rating.columns)
if __name__ == "__main__":
    main()