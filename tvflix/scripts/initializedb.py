import os
import sys
import transaction
import random
import string

from sqlalchemy import (
    engine_from_config,
    create_engine
    )
    
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..db.db_initialization import initialize_db


#generates randomly 64 long string
def apikey_generator(size=64, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))   

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')

    db_dir = str(engine) #get path for db
    #parsing
    db_dir = db_dir[db_dir.rfind('sqlite:///'):]
    db_dir = db_dir.replace("sqlite:///","")
    db_dir = db_dir.replace(")","")

    #create the database
    initialize_db(db_dir) 
    
    Base = automap_base()
    # reflect the tables
    Base.prepare(engine, reflect=True)
    
    # mapped classes are now created with names by default
    # matching that of the table name.
    User = Base.classes.Users
    Show = Base.classes.Shows  
    Tags = Base.classes.Tags
    #Show_tag = Base.classes.Shows_Tags #not working at the moment 
    Episode = Base.classes.Episodes
    Comment = Base.classes.Comments
    
    #creating a session
    session = Session(engine)
    
    with transaction.manager:
        user = User(username='test user', password='password', api_key = apikey_generator())
        session.add(user)
        session.commit()

