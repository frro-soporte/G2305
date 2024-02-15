import os
import secrets
from typing import List, Optional

from PIL import Image
from flask_mail import Message
from flask import current_app
from eggList import mail
from eggList.models.ciudad import Ciudad
from eggList.models.supermercado import Supermercado

import folium


def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = f"{random_hex}{f_ext}"
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def save_family_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = f"{random_hex}{f_ext}"
    picture_path = os.path.join(current_app.root_path, 'static/grupo_familiar_pics', picture_fn)
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def send_email(users, title, body):
    mail.connect()
    msg = Message(title, sender='nahuel.coronel@ymail.com', recipients= [user.email for user in users])
    msg.body = body
    mail.send(msg)

def generate_map(ciudad:Ciudad, supermercados:Optional[List[Supermercado]]=None, no_touch:bool = False):
    min_zoom = ciudad.min_zoom
    map = folium.Map(location=ciudad.get_coordinates(),
                     min_zoom=min_zoom, zoom_start=min_zoom,
                     no_touch = no_touch,

                     tiles="Cartodb Positron")


    if supermercados:
        for supermercado in supermercados:
            folium.Marker(supermercado.get_coordinates(),
                          ).add_to(map)

    map.get_root().render()

    header = map.get_root().header.render()

    body_html = map._repr_html_()

    script = map.get_root().script.render()

    return (header,body_html,script)