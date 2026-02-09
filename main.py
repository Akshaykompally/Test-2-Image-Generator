from flask import Flask,request,render_template,redirect,url_for
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import requests
import uuid
import os

ANIME_PROMPT = "Create an anime-style illustration featuring a vibrant, dynamic character.The character should have large, expressive eyes, intricate hairstyles, and a unique outfit that reflects their personality." \
               "The scene should be set in a fantastical environment, incorporating elements like lush landscapes, magical creatures, or futuristic cityscapes.Include a color palette that enhances the mood of the scene,"\
               "with bright and contrasting colors to give a sense of energy and life.The character's pose should convey movement and emotion, making them the focal point of the image.Add subtle details in the background " \
               "to enrich the narrative of the scene without overwhelming the main character."

CARTOON_PROMPT = "Design a lively and imaginative cartoon-style illustration showcasing. The image should embody a fun and imaginative atmosphere, utilizing bold colors and exaggerated features to enhance the cartoon aesthetic." \
                 "Include elements such as [insert specific details, e.g., a colorful background, playful expressions, dynamic poses]to bring the scene to life.Ensure the composition is balanced and eye-catching, appealing to a wide" \
                 " audience, particularly children.The style should reflect classic cartoon influences while incorporating modern design trends, with a focus on clarity and visual storytelling."

COMIC_PROMPT = "Create a comic strip that captures the essence of classic comic book art styles from the Golden Age of Comics.The strip should consist of four panels, each featuring dynamic characters engaged in an action-packed scene.Use bold," \
               " vibrant colors with heavy black outlines to enhance the visual impact.Incorporate speech bubbles with classic font styles for dialogue, ensuring that the text is clear and conveys the characters' emotions effectively.The characters" \
               " should exhibit exaggerated expressions and poses typical of the comic genre, and the background should include stylized elements that reflect the time period, such as retro cityscapes or dramatic landscapes.Ensure that the overall composition" \
               " and panel arrangement flow smoothly, guiding the reader's eye from one panel to the next while maintaining a sense of continuity in the storyline."



app = Flask(__name__)

app.secret_key = 'random'
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "@kshay03sep2004"
app.config['MYSQL_DB'] = "login_details"

mysql = MySQL(app)
login_manage = LoginManager()
login_manage.init_app(app)
bcrypt = Bcrypt(app)


@login_manage.user_loader
def load_user(user_id):
    return User.get(user_id)

class User(UserMixin):
    def __init__(self,user_id,first_name,last_name,email):
        self.id = user_id
        self.first = first_name
        self.last = last_name
        self.email = email

    @staticmethod
    def get(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT first_name,last_name,email FROM details where id = %s',(user_id,))
        res = cursor.fetchone()
        cursor.close()
        if res:
            return User(user_id,res[0],res[1],res[2])
        

@app.route('/')
def main_page():
    return render_template('login.html')



@app.route('/login', methods = ['POST','GET'])
def login_page():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()

        cursor.execute('SELECT id,first_name,last_name,password from details where email=%s',(email,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data and bcrypt.check_password_hash(user_data[3],password):
            user = User(user_data[0],user_data[1],user_data[2],user_data[3])
            login_user(user)
            return redirect(url_for('dash_board'))

    return render_template('login.html')


@app.route('/signup', methods = ['POST','GET'])
def signup():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO details (first_name,last_name,email,password) values (%s,%s,%s,%s)',(fname,lname,email,hashed_password))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('login_page'))

    return render_template('Signup.html')


@app.route('/dashboard', methods=['POST','GET'])
@login_required
def dash_board():
    image_url = None

    if request.method == 'POST':
        user_prompt = request.form['prompt']
        choice = request.form['choice']
        

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO prompts (text, type,email) VALUES ( %s,%s, %s)",(user_prompt, choice,current_user.email))
        mysql.connection.commit()
        cursor.close()

        if choice == 'anime':
            final_prompt = f"{user_prompt}, {ANIME_PROMPT}"
        elif choice == 'cartoon':
            final_prompt = f"{user_prompt}, {CARTOON_PROMPT}"
        else:
            final_prompt = f"{user_prompt}, {COMIC_PROMPT}"

        r = requests.post(
            "https://clipdrop-api.co/text-to-image/v1",
            files={"prompt": (None, final_prompt)},
            headers={
                "x-api-key": 'd0c2094f534eedeccc4563340951fb6b168bac73456ea827409cdb9a055368104ee64fbf376177cd0609f9c8eda2287c'
            }
        )

        if r.ok:
            filename = f"{uuid.uuid4().hex}.png"
            path = f"static/{filename}"

            with open(path, "wb") as f:
                f.write(r.content)

            image_url = path

    return render_template("Main.html", image_url=image_url)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login_page"))


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)


