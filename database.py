import sqlite3

con = sqlite3.connect("urls.db")

def init_db(con) -> bool: #creates the database and tables
	cur = con.cursor()	
	table_q = """
				CREATE TABLE IF NOT EXISTS urls (
					idx INT PRIMARY KEY,
					long_url TEXT,
					short_url TEXT
				)
	"""

	cur.execute(table_q)
	return True


def add_url(url_data: tuple) -> bool: # adds url to the databse
    sql = ''' INSERT INTO urls(idx,long_url,short_url)
              VALUES(?,?,?) '''
    last_index = last_id()
    idx = 1 if last_index is None else last_index + 1
    full_data = (idx, url_data[0], url_data[1]) 
    cur = con.cursor()
    cur.execute(sql, full_data)
    con.commit()

    return True

def get_data(): #gets all the url data
	cur = con.cursor()
	cur.execute('select idx, long_url, short_url from urls')
	rows = cur.fetchall()	 

	for row in rows:
		print(row)
 
def get_long_url(short_url: str) -> tuple:
    try:
        cur = con.cursor()
        cur.execute('select long_url from urls where short_url =?', (short_url,))
        row = cur.fetchone()
        if row:
            return row[0], None # Success: return URL
        return None, "Not found" # Return error instead of crashing
    except sqlite3.OperationalError as e:
        return None, e

def get_short_url(long_url: str) -> tuple: #gets the short url based on the long url
    try:
        cur = con.cursor()
        cur.execute('select short_url from urls where long_url =?', (long_url,))
        row = cur.fetchone()
        if row:
        	return row[0], None
        else:
        	return "error in get_short_url()", row
    except sqlite3.OperationalError as e:
        return None, e  

def last_id():
    cur = con.cursor()

    cur.execute("SELECT MAX(idx) FROM urls")
    result = cur.fetchone()
   
    return result[0] if result else None

def check_collision_long_url(url: str): # checks if the long url already exists in the data
    try:
        cur = con.cursor()
        cur.execute('select long_url from urls where long_url =?', (url,))
        row = cur.fetchone()
        if row:
        	#print(row[0])
        	short_url = get_short_url(row[0])
        	return short_url
        	#
        return False
    except sqlite3.OperationalError as e:
        return None, e

def check_collision_short_url(url: str) -> bool: # checks if the short url already exists in the data
    try:
        cur = con.cursor()
        cur.execute('select short_url from urls where short_url =?', (url,))
        row = cur.fetchone()
        if row:
        	return True
        return False
    except sqlite3.OperationalError as e:
        return None, e

init_db(con)
'''
url = ('long url', 'short')
add_url(con, url)
get_data(con)
redir = get_long_url("short")
print(redir)
'''
