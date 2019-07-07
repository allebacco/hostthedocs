import os
import sqlite3

from . import getconfig
from .entities import Project, Version


DB_FILENAME = os.path.join(getconfig.docfiles_dir, "database.sqlite")


if not os.path.exists(DB_FILENAME):

    conn = sqlite3.connect(DB_FILENAME)
    conn.executescript("""
        CREATE TABLE projects (name TEXT NOT NULL UNIQUE, description TEXT NOT NULL);
        CREATE TABLE versions (project_id INTEGER NOT NULL, version TEXT NOT NULL, url TEXT NOT NULL);

        CREATE UNIQUE INDEX project_version ON versions (project_id, version);
    """)
    conn.close()
    

def add_project(name: str, description: str):

    try:
        conn = sqlite3.connect(DB_FILENAME)
        conn.execute('INSERT INTO projects(name, description) VALUES(?,?)', (name, description))
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError:
        conn.close()
        return False

    return True


def get_projects():

    projects = list()

    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.execute('SELECT rowid, name, description FROM projects ORDER BY rowid ASC')
        for row in cursor.fetchall():
            projects.append(Project(row[0], row[1], row[2]))

        for project in projects:
            cursor = conn.execute('SELECT version, url FROM versions WHERE project_id=?', [project.rowid])
            versions = list()
            for row in cursor.fetchall():
                versions.append(Version(row[0], row[1]))
            project.add_versions(versions)

        conn.close()
    except sqlite3.DatabaseError:
        conn.close()

    return projects


def add_version(self, project: str, version: Version):

    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.execute('SELECT rowid FROM projects WHERE project=?')
        row = cursor.fetchone()
        if row is None:
            return False
        
        project_id = row[0]

        conn.execute(
            'INSERT OR REPLACE INTO versions(project_id, version, url) VALUES(?,?,?)', 
            [project_id, version.version, version.url]
        )

        conn.close()
    except sqlite3.DatabaseError:
        conn.close()

    return True

    
