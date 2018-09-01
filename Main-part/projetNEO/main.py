# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 23:15:20 2018

@author: Arthur & Camille & Jean-Baptiste
"""
#librairies
import os
from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from py2neo_marmiton import recette, etapes
from marmiton_ingredient import image_ingredient


html_str =""" 
<!doctype html>
<html>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" type="text/css" charset="utf-8">
<body>
<p>
Dans votre frigo, vous avez les ingrédients suivants : {{result}}.<br/><br/> <br/> 
Les plats que nous vous proposons sont :<ul style="list-style-type:square"> {0} </ul>.<br/><br/> <br/>
<p>Veuillez choisir une recette parmi les résultats :  
<form method="POST" action="http://localhost:5000/index">
<select name="nom" size="1">
{puces}
</select>
<input type = "submit" value = "submit" />
</form>
</p>
</body>
</html>"""


html_str_bis =""" 
<!doctype html>
<html>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" type="text/css" charset="utf-8">
<body>
<p> Vous avez choisi la recette suivante : {{camille}}.<br/><br/> <br/> 
Voici les étapes de la recette : <br/> <br/> 
<ul style="list-style-type:square">
{0}
</ul>
</p>
</body>
</html>"""

html_str_ter =""" 
<!DOCTYPE html>
<html>
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" type="text/css" charset="utf-8">
<body>
<p>Le nom de votre photo est : {{puces}}</p><br/><br/> <br/>
<p>Le nom de votre ingrédient est : {{marc}}</p><br/><br/> <br/>
Les plats que nous vous proposons sont :<ul style="list-style-type:square"> {0} </ul>.<br/><br/> <br/>
<p>Veuillez choisir une recette parmi les résultats :  
<form method="POST" action="http://localhost:5000/index">
<select name="nom" size="1">
{liens}
</select>
<input type = "submit" value = "submit" />
</form>
</p>
</body>
</html>"""


app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/')
def student():
   return render_template("student.html")

@app.route('/index',methods = ['POST', 'GET'])
def index():
   if request.method == 'POST':
      result_new = request.form['nom']#on récupère le nom de la recette dans la barre déroulante.
      instru = etapes(result_new)#on applique la fonction etapes de py2neo_marmiton.py à la recette sélectionnée.
      li = "<li>{0}</li>"#pour l'affichage des étapes sous forme d'énumération.
      subitems = [li.format(a) for a in instru]#pour l'affichage des étapes sous forme d'énumération.
      neo =  html_str_bis.format("".join(subitems))#on substitue ces valeurs dans la string html définie au début.
      neo = neo.replace("{", "{{")
      neo = neo.replace("}", "}}")
      f= open("templates/index.html","w",encoding='utf-8')#on définti un nouveau fichier html, christaline.html 
      f.write(neo)#on y enregistre la nouvelle string actualisée.
      f.close()#on ferme le fichier
   return render_template("index.html",camille = result_new)#on restitue le résultat et on remplace camille dans le html par
                                                               #result_new
                                                               
@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
      result = request.form#on récupère le résultat de la form dans student.html.
      ListeIngredient = result.getlist('ingredient')#on stocke le résultat dans une liste que l'on nomme ListeIngredient.
      #ListeIngredient = ", ".join(map(str,ListeIngredient))
      myList = []
      for ingredient in ListeIngredient:
          if len(ingredient) > 0:
              myList.append(ingredient)
              string_list = ", ".join(map(str,myList))#on fait cela pour obtenir quelque chose de plus propre pour l'affichage.
              stock = recette(myList)#on applique la fonction recette que l'on a définit dans py2neo_marmiton.py.
              #stock_bis = ", ".join(map(str,stock))
              li = "<li>{0}</li>"#pour l'affichage des recettes sous forme d'énumération.
              select = "<option>{0}</option>"#pour l'affichage des recettes dans une barre déroulante.
              subitems = [li.format(a) for a in stock]#pour l'affichage des recettes sous forme d'énumération.
              subitems_bis = [select.format(a) for a in stock]#pour l'affichage des recettes dans une barre déroulante.
              #subitems_bis = "".join(subitems_bis)
              carac = "".join(subitems_bis)#on concatène la liste dans une chaîne de caractères
              neo =  html_str.format("".join(subitems),puces = carac)#on substitue ces valeurs dans la string html définie au début.
              #,"".join(subitems_bis)
              #neo = neo.format("".join(subitems_bis))
              neo = neo.replace("{", "{{")
              neo = neo.replace("}", "}}")
              #print(neo)
              f= open("templates/christaline.html","w",encoding='utf-8')#on définti un nouveau fichier html, christaline.html 
              f.write(neo)#on y enregistre la nouvelle string actualisée.
              f.close()#on ferme le fichier
              #print html_str.format("".join(subitems))"""
    return render_template("christaline.html",result = string_list)
          

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        a = image_ingredient('..\\ProjetNEO\\static\\img\\'+filename)
        NewList = []
        NewList.append(a)
        stock = recette(NewList)
        li = "<li>{0}</li>"
        select = "<option>{0}</option>"
        subitems = [li.format(a) for a in stock]
        subitems_bis = [select.format(a) for a in stock]
        carac = "".join(subitems_bis)
        #subitems =", ".join(subitems)
        neo =  html_str_ter.format("".join(subitems),liens = carac)
        neo = neo.replace("{", "{{")
        neo = neo.replace("}", "}}")
        g= open("templates/download.html","w",encoding='utf-8')#on définti un nouveau fichier html, christaline.html 
        g.write(neo)#on y enregistre la nouvelle string actualisée.
        g.close()#on ferme le fichier
    return render_template("download.html",puces = filename, marc = a)


if __name__ == '__main__':
    app.run(debug=False)
    