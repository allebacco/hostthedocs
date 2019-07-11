import os
import sqlite3

from . import getconfig
from .entities import Project, Version


DB_FILENAME = os.path.join(getconfig.docfiles_dir, "database.sqlite")


if not os.path.exists(DB_FILENAME):

    conn = sqlite3.connect(DB_FILENAME)
    conn.executescript("""
        CREATE TABLE projects (
            name TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL,
            logo TEXT NOT NULL
        );

        CREATE TABLE versions (
            project_id INTEGER NOT NULL,
            version TEXT NOT NULL,
            url TEXT NOT NULL,
            UNIQUE(project_id, version)
        );
    """)
    conn.close()


def add_project(name: str, description: str, logo: str):

    try:
        conn = sqlite3.connect(DB_FILENAME)
        conn.execute('INSERT INTO projects(name, description, logo) VALUES(?,?,?)', (name, description, logo))
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
        cursor = conn.execute('SELECT rowid, name, description, logo FROM projects ORDER BY rowid ASC')
        for row in cursor.fetchall():
            projects.append(Project(row[0], row[1], row[2], row[3]))

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


def get_project(name: str) -> Project:

    project = None
    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.execute('SELECT rowid, name, description, logo FROM projects WHERE name = ?', [name])
        row = cursor.fetchone()
        if row is not None:
            project = Project(row[0], row[1], row[2], row[3])
            cursor = conn.execute('SELECT version, url FROM versions WHERE project_id=?', [project.rowid])
            versions = list()
            for row in cursor.fetchall():
                versions.append(Version(row[0], row[1]))
            project.add_versions(versions)

        conn.close()
    except sqlite3.DatabaseError:
        conn.close()

    return project


def update_project_description(project: str, new_description: str):

    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.execute('SELECT rowid FROM projects WHERE name=?', [project])
        row = cursor.fetchone()
        if row is None:
            return False

        project_id = row[0]

        conn.execute(
            'UPDATE projects SET description = ? WHERE rowid = ?',
            [new_description, project_id]
        )

        conn.commit()

        conn.close()
    except sqlite3.DatabaseError as e:
        print(e)
        conn.close()

    return True


def update_project_logo(project: str, new_logo: str):

    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.execute('SELECT rowid FROM projects WHERE name=?', [project])
        row = cursor.fetchone()
        if row is None:
            return False

        project_id = row[0]

        conn.execute(
            'UPDATE projects SET logo = ? WHERE rowid = ?',
            [new_logo, project_id]
        )

        conn.commit()

        conn.close()
    except sqlite3.DatabaseError as e:
        print(e)
        conn.close()

    return True


def add_version(project: str, version: Version):

    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.execute('SELECT rowid FROM projects WHERE name=?', [project])
        row = cursor.fetchone()
        if row is None:
            return False

        project_id = row[0]

        conn.execute(
            'INSERT OR REPLACE INTO versions(project_id, version, url) VALUES(?,?,?)',
            [project_id, version.version, version.url]
        )

        conn.commit()

        conn.close()
    except sqlite3.DatabaseError as e:
        print(e)
        conn.close()

    return True
