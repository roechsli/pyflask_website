# Module Imports
import mariadb
import sys

def connection():
	# Connect to MariaDB Platform
	try:
		conn = mariadb.connect(
			user="ikon2_db",
			password="",
			host="",
			port=3306,
			database="prev"

		)
		# Get Cursor
		cur = conn.cursor()
		return cur, conn
	except mariadb.Error as e:
		print(f"Error connecting to MariaDB Platform: {e}")
		sys.exit(1)
