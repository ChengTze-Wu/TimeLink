import mysql.connector
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        # connect to the database and store connection pools in the global variable g
        g.db = mysql.connector.connect(pool_name="timelink", pool_size=30, **current_app.config['DATABASE'])
        
    return g.db
  
      
def init_db():
    # connect to the database
    db = get_db()
    # create the database tables 
    with current_app.open_resource('schema.sql') as f:
        with db.cursor() as cursor:
            cursor.execute(f.read().decode('utf8'), multi=True)
        db.commit()
        
        
@click.command('init-db')
@with_appcontext
def init_db_command():
    # clear the existing data and create new tables
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.cli.add_command(init_db_command)