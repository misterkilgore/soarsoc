import os
import sqlite3

class DbHandler:
    def __init__(self, filepath):
        
        # Controlla il file del db
        if os.path.isfile(filepath):
            self.filepath = filepath
        else:
            print(f'Creato file {filepath}')
            self.filepath = filepath

        # Connetti con sqlite3
        self.connection = sqlite3.connect(self.filepath)
        self.cursor = self.connection.cursor()
        
    def show_records(self, table):
        
        # Faccio un semplice SELECT *
        
        sql = f'SELECT * FROM {table}'
        data = self.cursor.execute(sql)
        
        return data.fetchall()
       
        
    def insert_record(self, table, keys, values):
        if len(keys) != len(values):
            raise ValueError("'keys' e 'values' non hanno la stessa lunghezza")
        else:
            keys_string = '(' + ', '.join(keys) + ')'
            placeholders = "(" + ", ".join(["?"] * len(values)) + ")"
            sql = f'INSERT INTO {table} {keys_string} VALUES {placeholders}'
            self.cursor.execute(sql, values)
            self.connection.commit()
