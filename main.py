import webapp2
import MySQLdb
import passwords
import random
import cgi

form = cgi.FieldStorage()
conn = MySQLdb.connect(unix_socket = passwords.SQL_HOST,
			user = passwords.SQL_USER,
			passwd = passwords.SQL_PASSWD,
			db = "db1")

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		cookie = self.request.cookies.get("cookie_name")
		if cookie == None:
			id = "%032x" % random.getrandbits(128)
			user = None
		
			cursor = conn.cursor()
			cursor.execute("INSERT INTO sessions(sessionID, username) VALUES(%s, %s);",(id, user,))
			conn.commit()
			cursor.close()
			
			self.response.set_cookie("cookie_name", id, max_age=1800)

			self.response.write("""
			<html><body>
				<form action="" method="GET">
					<p>Enter a username:
					<input type="textarea" name="USER"></input>
					<button type="submit">Submit</button>
				</form>
			</body></html>
			""")
		else:
			if "USER" in form:
				user = form["USER"].value
		
				cursor = conn.cursor()
				cursor.execute("UPDATE sessions SET username=%s WHERE username=None;",(user,))
				conn.commit()
				cursor.close()
				
				cursor = conn.cursor()
				cursor.execute("INSERT INTO users(username, value) VALUES(%s, 0);",(user,))
				conn.commit()
				cursor.close()
				
				cursor = conn.cursor()
				cursor.execute("UPDATE users SET value=value+1;")
				new_id = cursor.lastrowid
				conn.commit()
				cursor.close()
				
				cursor = conn.cursor()
				cursor.execute("SELECT * FROM user WHERE id=%s;",(new_id,))
				results = cursor.fetchall()
				cursor.close()
				
				self.response.write("""
				<html><body>
					<form action="" method="GET">
						<p>Value: {}
						<input type="hidden" value=user></input>
						<button type="submit">Increment</button>
					</form>
				</body></html>
				""".format(results[2]))

app = webapp2.WSGIApplication([
	('/',MainPage),
], debug=True)
