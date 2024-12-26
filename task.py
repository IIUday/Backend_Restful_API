from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# Database connection
connection = pymysql.connect(
    host='sql12.freesqldatabase.com',
    user='sql12754200',
    password='dNSrQ2bbd6',
    database='sql12754200',
    cursorclass=pymysql.cursors.DictCursor
)

# Helper function to execute SQL queries
def execute_query(query, params=None, fetchone=False, fetchall=False):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if fetchone:
            return cursor.fetchone()
        if fetchall:
            return cursor.fetchall()
        connection.commit()

@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    try:
        query = """INSERT INTO recipes (title, making_time, serves, ingredients, cost)
                   VALUES (%s, %s, %s, %s, %s)"""
        execute_query(query, (data['title'], data['making_time'], data['serves'], data['ingredients'], data['cost']))
        return jsonify({
            "message": "Recipe successfully created!",
            "recipe": data
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/recipes', methods=['GET'])
def get_recipes():
    try:
        query = "SELECT * FROM recipes"
        recipes = execute_query(query, fetchall=True)
        return jsonify(recipes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    try:
        query = "SELECT * FROM recipes WHERE id = %s"
        recipe = execute_query(query, (id,), fetchone=True)
        if not recipe:
            return jsonify({"message": "Recipe not found"}), 404
        return jsonify(recipe), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/recipes/<int:id>', methods=['PATCH'])
def update_recipe(id):
    data = request.get_json()
    try:
        recipe = execute_query("SELECT * FROM recipes WHERE id = %s", (id,), fetchone=True)
        if not recipe:
            return jsonify({"message": "Recipe not found"}), 404

        query = """UPDATE recipes SET title = %s, making_time = %s, serves = %s, ingredients = %s, cost = %s
                   WHERE id = %s"""
        execute_query(query, (
            data.get('title', recipe['title']),
            data.get('making_time', recipe['making_time']),
            data.get('serves', recipe['serves']),
            data.get('ingredients', recipe['ingredients']),
            data.get('cost', recipe['cost']),
            id
        ))
        return jsonify({"message": "Recipe successfully updated!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    try:
        recipe = execute_query("SELECT * FROM recipes WHERE id = %s", (id,), fetchone=True)
        if not recipe:
            return jsonify({"message": "Recipe not found"}), 404

        query = "DELETE FROM recipes WHERE id = %s"
        execute_query(query, (id,))
        return jsonify({"message": "Recipe successfully deleted!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)