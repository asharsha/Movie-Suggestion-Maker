from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('movies_dataset.csv', low_memory=False)

@app.route('/', methods=['GET', 'POST'])
def movie_suggestions():
    if request.method == 'POST':
        # Get user input from the form
        user_genre = request.form['genre']

        # Filter movies by the selected genre
        genre_movies = df[df['genres'].str.contains(user_genre, case=False)]

        # Sort movies by popularity
        sorted_movies = genre_movies.sort_values(by='popularity', ascending=False)

        # Select the top ten movies
        top_ten = sorted_movies.head(10)

        # Select the remaining movies (after the top ten)
        remaining_movies = sorted_movies.iloc[10:]

        # Convert the results to a list of dictionaries
        top_ten_list = top_ten.to_dict(orient='records')
        remaining_list = remaining_movies.to_dict(orient='records')

        return render_template('movie_suggestions.html', user_genre=user_genre, top_ten=top_ten_list, remaining=remaining_list)

    return render_template('movie_suggestions.html')

if __name__ == '__main__':
    app.run(debug=True)
