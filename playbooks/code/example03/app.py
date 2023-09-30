'''
    AncientGods: Application to catalog AncientGods Information.
    export REDIS_OM_URL=redis://default:Ez5QrLhpQ+Nbl9FfCFnlOHu7@172.18.1.2:6300
    flask --app app run --host 0.0.0.0 --port 5300
    python3 -m pip install Flask==3.0.0 redis-om==0.2.1
'''

import datetime
import json
import os

from flask import Flask, send_from_directory, render_template, redirect, request

from redis_om import Migrator

from models import AncientGod, AccessHistory

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def root_route():
    return render_template('home.html',
                           title='Ancient Gods')

@app.route('/load_initial_data')
def load_initial_data():
    with open('all.json', encoding='utf8') as json_file:
        x=0
        all_data = json.load(json_file)
        for info in all_data:
            x += 1
            print(f'{info["name"]}={x}')
            greek_name = info['name']
            roman_name = info['romanName']
            if 'gender' in info:
                gender = info['gender']
            else:
                gender = 'Not Informed'
                print('Gender error')
            if 'description' in info:
                description = info['description']
            else:
                description = 'Not Informed'
                print('Desc error')
            if 'images' in info and \
                'regular' in info['images'] and \
                info['images']['regular'] != '':
                image_url = info['images']['regular']
            else:
                image_url = '/static/not_found.jpg'
                print('Image error')
            ancientgod = AncientGod(
                greek_name=greek_name,
                roman_name=roman_name,
                gender=gender,
                description=description,
                image_url=image_url,
                created_at=datetime.date.today(),
                updated_at=datetime.date.today()
            )
            ancientgod.save()
    Migrator().run()
    return redirect('/')

@app.route('/addform', methods=['GET'])
def addform():
    return render_template('addform.html',
                           tilte='Add new registry')

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        greek_name = request.form.get('greek_name')
        roman_name = request.form.get('roman_name')
        gender = request.form.get('gender')
        description = request.form.get('description')
        image_url = request.form.get('image_url')
    if request.method == 'GET':
        greek_name = request.args['greek_name']
        roman_name = request.args['roman_name']
        gender = request.args['gender']
        description = request.args['description']
        image_url = request.args['image_url']
    new_ancientgod = AncientGod(
        greek_name=greek_name,
        roman_name=roman_name,
        gender=gender,
        description=description,
        image_url=image_url,
        created_at=datetime.date.today(),
        updated_at=datetime.date.today(),
    )
    try:
        new_ancientgod.save()
        pk = new_ancientgod.pk
        new_access = AccessHistory(
                        ancientgod_pk=pk,
                        action='CREATE',
                        accessed_at=datetime.date.today()
                    )
        new_access.save()
    except:
        content = 'Error during add new registry'
        return render_template('error.html',
                                content=content)
    return redirect('/list')

@app.route('/list')
def list_registries():
    ''' Lists all registries of ancient_god table.
        Shows details, edit, and delete buttons to each registry.
    '''
    Migrator().run()
    registries = []
    list_of_registries = AncientGod.find(AncientGod.greek_name != '*').all()
    for registry in list_of_registries:
        registries += [ vars(registry) ]
    response =  render_template('list.html',
                                title='Ancient Gods',
                                registries=registries)
    new_access = AccessHistory(
                     ancientgod_pk='---ALL-PKS---',
                     action='LIST',
                     accessed_at=datetime.date.today()
                 )
    new_access.save()
    return response

@app.route('/details')
def details():
    ''' Shows a detail page including description and image.
        Shows details and delete buttons.
    '''
    title='Not found'
    registry = {
        'pk': '??',
        'greek_name': '?????',
        'roman_name': '?????',
        'description': 'Not found',
        'image_url': '?????',
        'updated_at': '?????',
        'gender': '?????',
        'created_at': '?????'
    }
    Migrator().run()
    if 'pk' in request.args:
        try:
            pk = request.args['pk']
        except:
            pk = '0'
        print(pk)
        registry = AncientGod.find(AncientGod.pk == pk).all()
        if  type(registry[0]) == AncientGod and 'greek_name' in vars(registry[0]) and 'roman_name' in vars(registry[0]):
            registry = registry[0]
            title=f'{vars(registry)["greek_name"]} / {vars(registry)["roman_name"]}'
            new_access = AccessHistory(
                             ancientgod_pk=pk,
                             action='DETAILS',
                             accessed_at=datetime.date.today()
                         )
            new_access.save()
    response = render_template('details.html',
                               title=title,
                               registry=registry)
    return response

@app.route('/delete')
def delete():
    ''' Deletes a registry from database.
        The button to delete is in list or details page.
    '''
    if 'pk' in request.args:
        pk = request.args['pk']
    else:
        pk = '0'
    try:
        AncientGod.delete(pk=pk)
        new_access = AccessHistory(
                         ancientgod_pk=pk,
                         action='DELETE',
                         accessed_at=datetime.date.today()
                     )
        new_access.save()
    except:
        content = f'Error during delete. Not found ID={pk}'
        return render_template('error.html',
                               content=content)
    return redirect('/list')


@app.route('/editform', methods=['GET'])
def editform():
    ''' Creates a form with the registry information to edit.
        If the route was opened without correct id, not found information will be displayed.
    '''
    title='Not found'
    registry = {
        'id': '??',
        'greek_name': '?????',
        'roman_name': '?????',
        'description': 'Not found',
        'image_url': '?????',
        'updated_at': '?????',
        'gender': '?????',
        'created_at': '?????'
    }
    response = render_template('editform.html',
                            title=title,
                            registry=registry)
    if 'pk' in request.args:
        print('if pk in request.args: TRUE')
        try:
            pk = request.args['pk']
        except:
            pk = '0'
        print(pk)
        registry = AncientGod.find(AncientGod.pk == pk).all()
        if  type(registry[0]) == AncientGod and 'greek_name' in vars(registry[0]) and 'roman_name' in vars(registry[0]):
            registry = registry[0]
            title=f'{vars(registry)["greek_name"]} / {vars(registry)["roman_name"]}'
            response = render_template('editform.html',
                                       title=title,
                                       registry=registry)
    else:
        content = f'Error during edit. Not found ID={request.args["id"]}'
        return render_template('error.html',
                                content=content)
    return response

@app.route('/edit', methods=['GET','POST'])
def edit():
    ''' Receives information from form (editform) and process.
        Redirects to /list if everyting is allright.
    '''
    if request.method == 'POST':
        try:
            pk = request.form.get('pk')
        except:
            content = 'Error during edit. PK is incorrect.'
            return render_template('error.html', content=content)
        greek_name = request.form.get('greek_name')
        roman_name = request.form.get('roman_name')
        gender = request.form.get('gender')
        description = request.form.get('description')
        image_url = request.form.get('image_url')
    if request.method == 'GET':
        try:
            pk = int(request.args['pk'])
        except:
            content = 'Error during edit. PK is incorrect.'
            return render_template('error.html', content=content)
        greek_name = request.args['greek_name']
        roman_name = request.args['roman_name']
        gender = request.args['gender']
        description = request.args['description']
        image_url = request.args['image_url']
    registry = AncientGod.find(AncientGod.pk == pk).all()
    if  type(registry[0]) == AncientGod and 'greek_name' in vars(registry[0]) and 'roman_name' in vars(registry[0]):
        registry[0].greek_name = greek_name
        registry[0].roman_name = roman_name
        registry[0].gender = gender
        registry[0].description = description
        registry[0].image_url = image_url
        registry[0].save()
        new_access = AccessHistory(
                        ancientgod_pk=pk,
                        action='EDIT',
                        accessed_at=datetime.date.today()
                    )
    else:
        content = f'Error during edit. Not found PK={pk}'
        return render_template('error.html',
                                content=content)
    new_access.save()
    return redirect('/list')

@app.route('/listhistory')
def list_history():
    ''' Shows the list of operations history. '''
    histories = []
    list_of_histories = AccessHistory.find(AccessHistory.pk != '0').all()
    for history in list_of_histories:
        histories += [ vars(history) ]
    total_operations = len(list_of_histories)
    create_operations = len(AccessHistory.find(AccessHistory.action == 'CREATE').all())
    details_operations = len(AccessHistory.find(AccessHistory.action == 'DETAILS').all())
    edit_operations = len(AccessHistory.find(AccessHistory.action == 'EDIT').all())
    delete_operations = len(AccessHistory.find(AccessHistory.action == 'DELETE').all())
    list_operations = len(AccessHistory.find(AccessHistory.action == 'LIST').all())

    return render_template('listhistory.html',
                           title='History List',
                           registries=histories,
                           total_operations=total_operations,
                           create_operations=create_operations,
                           details_operations=details_operations,
                           edit_operations=edit_operations,
                           delete_operations=delete_operations,
                           list_operations=list_operations)

