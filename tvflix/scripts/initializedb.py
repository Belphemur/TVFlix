#-*- coding: utf-8 -*-
import os
import sys
import transaction
import random
import string

from datetime import date, datetime, timedelta

from sqlalchemy import (
    engine_from_config,
    )
    
from ..models import Base, Session
from ..models.show import Show
from ..models.episode import Episode
from ..models.user import User
from ..models.comment import Comment
from ..models.tag import Tag
from ..models.show_tag import Shows_Tag



from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..db.db_initialization import initialize_db

defaultSummary = u'''Default summary. Having agreed to become the King’s Hand, Ned leaves Winterfell with daughters Sansa and Arya,
while Catelyn stays behind in Winterfell. Jon Snow heads north to join the brotherhood of the Night’s Watch.
Tyrion decides to forego the trip south with his family, instead joining Jon in the entourage heading to the Wall.
Viserys bides his time in hopes of winning back the throne, while Daenerys focuses her attention on learning how 
to please her new husband, Drogo.'''.replace("\n", "")
            
#defaultSummary = defaultSummary.replace("\n", "")
            
episodeList = ["Lord Snow", "Cripples, Bastards, and Broken Things", "The Wolf and the Lion", "A Golden Crown",
            "You Win or You Die", "The Pointy End", "Baelor", "Fire and Blood"]

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

    #create the database from premade schema
    initialize_db(db_dir)
    
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    from ..models.episode_showlabel import Episode_ShowLabel
    
    #lets add users
    with transaction.manager:
        user1 = User(username = 'test user', password = 'password', api_key = apikey_generator(), admin=False)
        user2 = User(username = 'Antoine', password = 'password', api_key =  apikey_generator(), admin=True)
        user3 = User(username = 'admin', password = 'password', api_key = 'admin', admin=True)
        user4 = User(username = 'user', password = 'password', api_key = 'user', admin=False)
        Session.add(user1)
        Session.add(user2)
        Session.add(user3)
        Session.add(user4)
      
    #looks stupid but what can you do about when you are lazy  
    summary1 = u'''Seven noble families fight for control of the mythical land of Westeros. 
Friction between the houses leads to full-scale war. All while a very ancient
evil awakens in the farthest north. Amidst the war, a neglected military order 
of misfits, the Night's Watch, is all that stands between the realms 
of men and icy horrors beyond.'''.replace("\n", "")
                            
    summary2 = u'''Charlie is a well-to-do bachelor with a house at the beach, a Jaguar in the front,
and an easy way with women. His casual Malibu lifestyle is interrupted when his tightly 
wound brother Alan, who's facing a divorce, and his son Jake, come to live with him. 
Together, these two and a half men confront the challenges of growing up; finally. 
Complicating matters are the brothers' self-obsessed, controlling mother, Evelyn, 
Alan's estranged wife, Judith and Charlie's crazy neighbor Rose, who wants to be a part 
of his life and is willing to do anything to be around. After the death of his brother,
Alan Harper meets and befriends a lonely young man named Walden Schmidt who turns out to be
a billionaire. Unable to afford his brother's home, Alan sells Walden the house, 
and as a way of showing his gratitude, Walden allows Alan and his son Jake to move in with him.'''.replace("\n", "")
                            
    summary3 = u'''Set in Springfield, the average American town, 
the show focuses on the antics and everyday adventures of the Simpson family; 
Homer, Marge, Bart, Lisa and Maggie, as well as a virtual cast of thousands. 
Since the beginning, the series has been a pop culture icon, attracting hundreds 
of celebrities to guest star. The show has also made name for itself in its fearless 
satirical take on politics, media and American life in general. '''.replace("\n", "")
      
    #Shows
    with transaction.manager:
        show1 = Show(showlabel='game-of-thrones', title='Game of Thrones',
                    start_year= 2009, end_year= 2016, bcast_day=6, 
                    summary= summary1, channel="HBO")
                    
        show2 = Show(showlabel='two-and-half-men', title='Two and half men',
                    start_year= 2003, end_year=None, bcast_day=0, 
                    summary= summary2, channel="CBS")
                    
        show3 = Show(showlabel='the-simpsons', title='The simpsons',
                    start_year=1989, end_year=None, bcast_day=5, 
                    summary= summary3, channel="FOX")
                    
        Session.add(show1)
        Session.add(show2)
        Session.add(show3)
        
    #Episodes
    with transaction.manager:
        session = Session()
        epi1 = Episode(show_id=1, title = "Winter is coming", season = 1, number = 1,
                        bcast_date = datetime.strptime('20110418', "%Y%m%d").date(), 
                        summary = u'''Ned Stark, Lord of Winterfell learns that his mentor, Jon Arryn,
has died and that King Robert is on his way north to offer Ned Arryn’s
position as the King’s Hand. Across the Narrow Sea in Pentos,
Viserys Targaryen plans to wed his sister Daenerys to the nomadic Dothraki warrior leader,
Khal Drogo to forge an alliance to take the throne.'''.replace("\n", "")
                                )

        epi2 = Episode(show_id=1, title = "The Kingsroad", season = 1, number = 2,
                        bcast_date = datetime.strptime('20110425', "%Y%m%d").date(), summary = defaultSummary)

        epi3 = Episode(show_id=1, title = "Lord Snow 2", season = 2, number = 1,
                        bcast_date = datetime.strptime('20120425', "%Y%m%d").date(), summary = defaultSummary)

        Session.add(epi1)
        Session.add(epi2)
        Session.add(epi3)
        
        #lazy episode adding to game of thrones
        dateSeq = datetime.strptime('20110502', "%Y%m%d").date()
        num = 3
        for i in episodeList:
            epi = Episode(show_id=1, title = i, season = 1, number = num,
                        bcast_date = dateSeq, summary = defaultSummary)
                        
            Session.add(epi)
            
            dateSeq = dateSeq + timedelta(days=7)
            num += 1
        
    #Comments
    with transaction.manager:
        com1 = Comment(user_id = 2, show_id = 1, comment = "OH god no, why everyone keeps dying!??!! Bad show",
                        posted = datetime.now(), updated = None)
                        
        com2 = Comment(user_id = 1, show_id = 1, comment = "buhahaaa",
                        posted = datetime.now(), updated = None)
                        
        Session.add(com1)
        Session.add(com2)
        
    with transaction.manager:
        tag1 = Tag(name = 'Drama')
        tag2 = Tag(name = 'Nudity')
        
        Session.add(tag1)
        Session.add(tag2)
        
    #linking the tags and shows
    with transaction.manager:
        conn = engine.connect()
        conn.execute(Shows_Tag.insert(),[
            {'show_id': 1, 'tag_id': 1},
            {'show_id': 1, 'tag_id': 2},
            {'show_id': 2, 'tag_id': 1}])

        conn.close()
