#!/usr/bin/env python

import os, sys, time , MySQLdb

def recursive_path_generator(root):
    for path, subdirs, files in os.walk(root):
        for name in files:
            yield os.path.join(path, name)
        for folder in subdirs:
            yield os.path.join(path, folder)   

def files_to_timestamp(root):
    return dict ((f, os.path.getmtime(f)) for f in recursive_path_generator(root))

if __name__ == "__main__":

    
    db = MySQLdb.connect("localhost","root","root","test" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    sql = """CREATE TABLE files (
         id INT PRIMARY KEY  AUTO_INCREMENT,
         file_name  VARCHAR(100),
         comment  VARCHAR(100) )"""

    cursor.execute(sql)


    def query(file_name, comment):
        sql = """INSERT INTO files(file_name, comment) 
        VALUES ('{}','{}')""".format(file_name, comment)
        try:
           # Execute the SQL command
           cursor.execute(sql)
           # Commit your changes in the database
           db.commit()
        except:
           db.rollback()

    path_to_watch = "."
    #print "Watching ", path_to_watch

    before = files_to_timestamp(path_to_watch)
    #print "before...", before

    while 1:
        time.sleep (3)
        after = files_to_timestamp(path_to_watch)
        #print "after...", after

       # added = [f for f in after.keys() if not f in before.keys()]
        added = []
        renamed = []
        for f, ts in after.items():
            #print f, ts
            if not f in before.keys():
                if len(after) == len(before):
                    renamed.append(f)
                else:
                    added.append(f)


        removed = [f for f in before.keys() if not f in after.keys()]
        modified = []

        for f in before.keys():
            if not f in removed:
                if os.path.getmtime(f) != before.get(f):
                    modified.append(f)

        for file_name in added:
            query(file_name, "Added")

        for file_name in removed:
            query(file_name, "Removed")

        for file_name in modified:
            query(file_name, "Modified")

        for file_name in renamed:
            query(file_name, "Renamed")

        if added: print "Added: ", ", ".join(added)
        if removed: print "Removed: ", ", ".join(removed)
        if modified: print "Modified ", ", ".join(modified)
        if renamed: print "Renamed ", ", ".join(renamed)
        
        before = after
