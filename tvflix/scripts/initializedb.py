import os
import sys
import transaction
import random
import string

from datetime import date, datetime

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
    
    #lets add users
    with transaction.manager:
        user1 = User(username='test user', password='password', api_key = apikey_generator())
        user2 = User(username='Antoine', password='password', api_key = apikey_generator())
        session.add(user1)
        session.add(user2)
        session.commit()
      
    #Shows
    with transaction.manager:
        show1 = Show(showlabel='game-of-thrones', title='Game of Thrones',
                    start_year= 2009, end_year= 2016, bcast_day=6, summary="Everybody dies", channel="HBO")
                    
        show2 = Show(showlabel='two-and-half-men', title='Two and half men',
                    start_year= 2004, end_year=None, bcast_day=0, 
                    summary="Fun guy, less fun guy and annoying kid show", channel="bcc")
                    
        show3 = Show(showlabel='simpsons', title='The simpsons',
                    start_year= 2001, end_year=None, bcast_day=0, 
                    summary="Yellow folks but they are not Asians", channel="MTV")
                    
        session.add(show1)
        session.add(show2)
        session.add(show3)
        session.commit()
        
    #Episodes
    with transaction.manager:
        epi1 = Episode(show_id=1, title = "everybody dies 1", season = 1, number = 1, 
                        bcast_date = date.today(), summary = 'Series starts, everybody are still alive')
                        
        epi2 = Episode(show_id=1, title = "tits", season = 1, number = 2, 
                        bcast_date = date.today(), summary = 'Just boobs')
                        
        epi3 = Episode(show_id=1, title = "Dragons", season = 2, number = 1, 
                        bcast_date = date.today(), summary = 'Boobs and dragons')
                        
        session.add(epi1)
        session.add(epi2)
        session.add(epi3)
        session.commit()
                        
    #Comments
    with transaction.manager:
        com1 = Comment(user_id = 2, show_id = 1, comment = "OH god no, why everyone keeps dying!??!! Bad show",
                        posted = datetime.now(), updated = None)
                        
        com2 = Comment(user_id = 1, show_id = 1, comment = "buhahaaa",
                        posted = datetime.now(), updated = None)
                        
        session.add(com1)
        session.add(com2)
        session.commit()
        
        
    

