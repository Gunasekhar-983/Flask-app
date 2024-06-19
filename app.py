from flask import Flask, render_template, request, jsonify, send_from_directory
import pickle

app = Flask(__name__)

data = pickle.load(open('new_df.pkl','rb'))
similarity = pickle.load(open('similarities.pkl', 'rb'))

def recommend(course_name):
    try:
        idx = data[data['Course Name'].str.contains(course_name, case=False, na=False)].index[0]
    except IndexError:
        return f"No course found with name containing '{course_name}'"

    sim_scores = list(enumerate(similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:7]

    recommended = [{"name": data.iloc[i[0]]['Course Name'], "url": data.iloc[i[0]]['Course URL']} for i in sim_scores]
    return recommended

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_courses', methods=['GET'])
def search_courses(): 
    query = request.args.get('query', '').lower()
    matching_courses = data[data['Course Name'].str.lower().str.contains(query)]['Course Name'].tolist()
    return jsonify(matching_courses[:10])

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    if request.method == 'POST':
        course_name = request.form['course_name']
        recommendations = recommend(course_name)
        return jsonify(recommendations)

@app.route('/static/Course_recommendation.csv')
def get_csv():
    return send_from_directory(app.static_folder, 'Course_recommendation.csv')

if __name__ == '__main__':
    app.run(debug=True)