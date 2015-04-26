# -*- coding: utf-8 -*-
import sqlite3
from db.models import Episode, Show, Config

__all__ = ['Queries']


class Queries(object):
    def __init__(self, conn):
        self.conn = conn

    def all_the_shows(self):
        c = self.conn.cursor()
        try:
            c.execute("""
                SELECT id, name, regexp_filter, min_size, max_size
                FROM shows
                ORDER BY name""")
            for row in c:
                yield Show(*row)
        finally:
            c.close()

    def find_episode_by_number(self, show_name, episode_number):
        c = self.conn.cursor()
        try:
            c.execute("""
                SELECT episodes.id, episodes.show_id, episodes.name, episodes.url, episodes.filename, episodes.torrent, episodes.size, episodes.queued, episodes.downloaded
                      FROM episodes, shows
                      WHERE shows.name = ? AND shows.id = episodes.show_id AND episodes.name = ?
                      ORDER BY episodes.name""", (show_name, episode_number))
            row = c.fetchone()
            if row is None:
                return None
            return Episode(show_name, *row)
        finally:
            c.close()

    def save_episode(self, episode):
        c = self.conn.cursor()
        try:
            c.execute("""
                INSERT INTO episodes
                      SELECT episodes.id, episodes.show_id, episodes.name, episodes.url, episodes.filename, episodes.torrent, episodes.size, episodes.queued, episodes.downloaded
                      VALUES ()
                      FROM episodes, shows
                      WHERE shows.name = ? AND shows.id = episodes.show_id AND episodes.name = ?
                      ORDER BY episodes.name""", (show_name, episode_number))
            # TODO: update the ID
            if row is None:
                return None
        finally:
            c.close()

    def episodes_by_show(self, show_name):
        c = self.conn.cursor()
        try:
            c.execute("""
                SELECT episodes.id, episodes.show_id, episodes.name, episodes.url, episodes.filename, episodes.torrent, episodes.size, episodes.queued, episodes.downloaded
                      FROM episodes, shows
                      WHERE shows.name = ? AND shows.id = episodes.show_id
                      ORDER BY episodes.name""", (show_name, ))
            for row in c.fetchall():
                yield Episode(show_name, *row)
        finally:
            c.close()

    def episodes_not_queued(self):
        c = self.conn.cursor()
        try:
            c.execute("""
                SELECT shows.name, episodes.id, episodes.show_id, episodes.name, episodes.url, episodes.filename, episodes.torrent, episodes.size, episodes.queued, episodes.downloaded
                      FROM episodes, shows
                      WHERE episodes.queued = 0 AND shows.id = episodes.show_id
                      ORDER BY episodes.name""")
            for row in c.fetchall():
                yield Episode(*row)
        finally:
            c.close()

    def all_the_config_vars(self):
        c = self.conn.cursor()
        try:
            c.execute("""
                SELECT id, name, regexp_filter, min_size, max_size
                FROM shows
                ORDER BY name""")
            for row in c:
                yield Show(*row)
        finally:
            c.close()
