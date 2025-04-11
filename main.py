import requests
import pandas as pd
import json
from textblob import TextBlob

def main():
    def fetch_professor_data(professor_name):
        url = f"https://api.planetterp.com/v1/professor?name={professor_name}&reviews=true"
        grade_url = f"https://planetterp.com/api/v1/grades?professor={professor_name}"
        response = requests.get(url)
        grade_response = requests.get(grade_url)
        if (response.status_code == 200) and (grade_response.status_code == 200):
            print(f"Fetched data from {url}")
            print(f"Fetched data from {grade_url}")
            return (response.json(), grade_response.json())
        else:
            return ({"error": f"Failed to fetch data. Status code: {response.status_code}"}, {"error": f"Failed to fetch data. Status code: {grade_response.status_code}"})

    professor_name = "Maksym Morawski"  # Replace with the desired professor's name

    gpa_map = {
    "A+": 4.0, "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D+": 1.3, "D": 1.0, "D-": 0.7,
    "F": 0.0
}
    test_professors = [
        "Maksym Morawski",
        "Shane Walsh",
        "Leigh Soares",
        "Susan Pramschufer",
        "Asim Ali",
        "Becky Epanchin-Niell",
        "Billie Ray",
        "James Hunt",
        "Melissa Hayes-Gehrke",
        "Leslie Pick",
        "Jacob Coutts",
        "Bailey Kier",
        "Humberto Coronado",
        "Daniel Sidman",
        "Justine DeCamillis",
        "Sarah Kilmer",
        "Andre Tits",
        "Cynthia Kershaw",
        "Ebonie Johnson Cooper",
        "Emily Dobson",
        "Martha Nell Smith",
        "Joseph Falvo",
        "Madeline Hsu",
        "Antoine Borrut",
        "Michel Cukier"
    ]
    
    def calc_sentiment(text):
        analysis = TextBlob(text)
        return analysis.sentiment.polarity
    
    def calculate_gpa_by_course(professor_grades):
        df = pd.DataFrame(professor_grades)
        
        # Keep only relevant GPA-related grade columns
        grade_cols = [g for g in gpa_map if g in df.columns]

        # Melt to long format: one row per grade per course
        long_df = df.melt(
            id_vars=["course", "professor"],
            value_vars=grade_cols,
            var_name="grade",
            value_name="count"
        )

        # Calculate GPA points for each row
        long_df["gpa_points"] = long_df["count"] * long_df["grade"].map(gpa_map)

        # Group by course and professor, sum everything
        gpa_summary = long_df.groupby(["professor", "course"]).agg(
            total_points=("gpa_points", "sum"),
            total_grades=("count", "sum")
        ).reset_index()

        # Final GPA calculation
        gpa_summary["gpa"] = gpa_summary["total_points"] / gpa_summary["total_grades"]
        print(gpa_summary)
        return pd.DataFrame(gpa_summary, columns=["professor", "course", "gpa", "total_points", "total_grades"])
    
    # Also test with this:
    # def normalized_polarity(text):
    # blob = TextBlob(text)
    # sentiment_words = [word for word in blob.words if TextBlob(word).sentiment.polarity != 0]
    # return blob.sentiment.polarity / max(len(sentiment_words), 1)
    
    df = pd.DataFrame()
    df_grades = pd.DataFrame()

    for professor_name in test_professors: 
         professor_data, professor_grades = fetch_professor_data(professor_name)
         if "reviews" in professor_data:
             professor_reviews = pd.DataFrame(professor_data["reviews"])
             df = pd.concat([df, professor_reviews], ignore_index=True)
         if professor_grades:
             grade_data = calculate_gpa_by_course(professor_grades)
             df_grades = pd.concat([df_grades, grade_data], ignore_index=True)

    # df.to_csv("test_professor_reviews.csv", index=False)
    # print("test data saved")

    df = pd.read_csv("all_professors_reviews.csv")
    # Drops rating for training

    df_no_rating = df.drop("rating", axis=1)

    # Adds sentiment column
    df['sentiment'] = df['review'].apply(calc_sentiment)
    # Adds columns with just the length of each review (maybe length is correlated with a good/bad review??)
    df['r_length'] = df['review'].apply(len)

    df_no_rating = df.drop("rating", axis=1)

    df.to_csv("processed_professor_reviews.csv", index=False)
    df_grades.to_csv("processed_professor_grades.csv", index=False)

if __name__ == "__main__":
    main()