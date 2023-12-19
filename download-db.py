import mysql.connector
import pandas as pd
# vars----------------------------
no_of_rows = 1000
filename = 'animedb.csv'
# --------------------------------

conn = mysql.connector.connect(
            host = 'aws.connect.psdb.cloud',
            user = 'xfroz16rd1lxpsjeh5kd',
            password = 'pscale_pw_DyTXiWGUofR62taIKiJ5Wtuwq1GXluj7r2ntEOhzOVK',
            database = 'anime'
        )
curr = conn.cursor()
curr.execute("SELECT * FROM anime")
raw_data = curr.fetchall()
# print(raw_data)
df = pd.DataFrame(raw_data, columns=['Name', 'Aired', 'Broadcast', 'Duration', 'Status', 'Type', 'Premiered', 'Episodes', 'Rating', 'Genres', 'Licensors', 'Producers', 'Studios', 'Members', 'Favorites'])
df = df.sample(frac=1)
df.loc[:no_of_rows].to_csv(filename, index=None)

print(f'data downloaded as {filename}')