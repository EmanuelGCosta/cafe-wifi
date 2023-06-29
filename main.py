from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField , SubmitField, SelectField
from wtforms.validators import DataRequired, URL, NumberRange
from dotenv import load_dotenv
from os import environ
import csv


app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = environ.get('key')
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Nome da cafeteria', validators=[DataRequired()])
    local = StringField('URL do local', validators=[DataRequired(), URL(message="URL invalida")])
    abre = IntegerField('Horário que Abre (Apenas números)', validators=[DataRequired(), NumberRange(min=0, max=24)])
    fecha = IntegerField('Horário que fecha (Apenas números)', validators=[DataRequired(), NumberRange(min=0, max=24)])
    cafe_nota = SelectField('Classificação do Café', choices=["☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"], validators=[DataRequired()])
    wifi_nota = SelectField('Classificação do Wifi', choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"], validators=[DataRequired()])
    tomadas_nota = SelectField('Classificação das tomadas', choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"], validators=[DataRequired()])
    submit = SubmitField('Enviar')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", mode="a", encoding="UTF-8") as csv_file:
            print(form.cafe)

            csv_file.write(f"\n{form.cafe.data},"
                           f"{form.local.data},"
                           f"{form.abre.data},"
                           f"{form.fecha.data},"
                           f"{form.cafe_nota.data},"
                           f"{form.wifi_nota.data},"
                           f"{form.tomadas_nota.data}")
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="UTF-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)