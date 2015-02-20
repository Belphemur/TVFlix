from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from tvflix import engine

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
Session = Session(engine)