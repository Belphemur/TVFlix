import sys, os
import sqlite3

#creating a db from schema file
#schema file has to be in same dir than database, and named as: sql_schema.sql
#existing db has to be deleted before we can create a new db
def initialize_db(path):
    
    def __init__(self, schema, path):
        self.schema = schema
        self.path = path
    
    
    def readSchema(path):
        script_dir = path #script path path
        #remove filename
        script_dir = script_dir[:script_dir.rfind('/')]
        initialize_db.path = script_dir
        
        db_schema = os.path.join(script_dir, "sql_schema.sql") 
              
        if not os.path.isfile(db_schema):
            return False
            
        else:    
            #open, read and close file    
            with open(db_schema) as file:
                #save file content to an object
                content = file.readlines()
                
            #iterating and parsing a list 
            schema = '' #empty string
            for line in content:
                schema = schema + line
                
            #encoding the string to utf-8    
            schema = unicode(schema, "utf-8")

            #saving the schema to object
            initialize_db.schema = schema
                
            return True


    def checkdb():
        db_filename = 'tvflix.db'

        db = os.path.join(initialize_db.path, db_filename)
        
        #check if there is a database file already
        if not os.path.isfile(db):
            return True
        
        
    def createdb():
        db_filename = 'tvflix.db' 
        database = os.path.join(initialize_db.path, db_filename)
        
        #create a db file
        new_db = not os.path.exists(database)

        with sqlite3.connect(database) as conn:
            if new_db: 
                conn.executescript(initialize_db.schema)
                
                print "Database created!"
                return True

        
    if not readSchema(path):
        sys.exit("No schema file found!")
    if  not checkdb():
        sys.exit("Database exists, please detele it before creating a new one")
    if not createdb():
        sys.exit("Ooops, could not create a database")
    
        
        