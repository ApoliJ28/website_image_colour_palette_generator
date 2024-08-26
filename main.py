from flask import Flask, render_template, request
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import os

app = Flask(__name__)

DIR_IMAGE_DEFAULT = 'static/img/coffe.jpg'
UPLOAD_FOLDER =  'static/img/'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Crear el directorio si no existe

def get_colors_image_hex_top_10(upload_image=None) -> list:
    if not upload_image:
        image = Image.open(DIR_IMAGE_DEFAULT).convert('RGB')
    else:
        image = Image.open(upload_image).convert('RGB')

    # Redimensionar la imagen para acelerar el procesamiento (opcional)
    image = image.resize((100, 100))

    # Convertir la imagen a un array numpy
    image_np = np.array(image)

    # Reshape la imagen para que cada fila sea un color (3 valores RGB por fila)
    pixels = image_np.reshape(-1, 3)

    # Usar K-means clustering para encontrar los colores más comunes
    kmeans = KMeans(n_clusters=10, random_state=0).fit(pixels)

    # Obtener los colores de los clusters
    colors = kmeans.cluster_centers_

    # Convertir los colores a formato hexadecimal
    hex_colors = ['#{:02x}{:02x}{:02x}'.format(int(color[0]), int(color[1]), int(color[2])) for color in colors]
    
    return hex_colors

@app.route("/", methods=['GET', 'POST'])
def home():
    is_form_success = False
    image_path = os.path.join(UPLOAD_FOLDER, 'uploaded_image.jpg')
    
    if request.method == 'POST':
        
        img = request.files.get('image')
        
        if img:
            
            list_colors_hex = get_colors_image_hex_top_10(upload_image=img)
            is_form_success = True            
            
            Image.open(img).save(image_path) # Guardamos la imagen
            
        else:
            list_colors_hex = get_colors_image_hex_top_10()
        
        list_colors_hex=get_colors_image_hex_top_10(upload_image=img)

    else:
        list_colors_hex = get_colors_image_hex_top_10()
    
    return render_template('index.html', colors_hex = list_colors_hex, is_form_success = is_form_success)

if __name__ == '__main__':
    app.run()
