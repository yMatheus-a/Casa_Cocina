from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from flask_menu import register_menu
from .models import Note
from . import db
import json
import os

views = Blueprint('views', __name__)

# Caminho para o arquivo JSON de receitas fit
recipes_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/js/recipes_fit.json')

# Carregar dados de receitas do arquivo JSON
with open(recipes_path, 'r', encoding='utf-8') as file:
    recipes = json.load(file)

@views.route('/', methods=['GET', 'POST'])
@register_menu(views, '.', 'Home')
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()

    return jsonify({})

@views.route('/search')
def search():
    query = request.args.get('query')
    return redirect(url_for('views.results', query=query))

@views.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    suggestions = [item for item in recipes if search.lower() in item.lower()]
    return jsonify(suggestions)

@views.route('/results')
def results():
    query = request.args.get('query')
    if query in recipes:
        return redirect(recipes[query])
    else:
        flash('Receita não encontrada!', category='error')
        return redirect(url_for('views.home'))

@views.route('/receita/chips-batata-doce')
def chips_batata_doce():
    return render_template('receitas/chips_batata_doce.html', user=current_user)

@views.route('/receita/salada-de-quinoa-com-legumes')
def salada_de_quinoa():
    return render_template('receitas/salada_de_quinoa.html', user=current_user)

@views.route('/receita/salada-de-frutas-e-iogurte')
def salada_de_frutas_e_iogurte():
    return render_template('receitas/salada_de_frutas_e_iogurte.html', user=current_user)

@views.route('/noticias')
def noticias():
    return render_template('noticias.html')

# Novas rotas com Flask-Menu
@views.route('/perfil')
@register_menu(views, '.perfil', 'Seu Perfil')
@login_required
def perfil():
    return render_template('perfil.html', user=current_user)

@views.route('/minhas-receitas')
@register_menu(views, '.minhas_receitas', 'Suas Receitas')
@login_required
def minhas_receitas():
    return render_template('minhas_receitas.html', user=current_user)

@views.route('/consulta')
@register_menu(views, '.consulta', 'Fazer uma Consulta')
@login_required
def consulta():
    return render_template('consulta.html', user=current_user)
