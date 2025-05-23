import asyncio
import tornado
import json

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)




from sqlalchemy import create_engine,inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

username=""
password=""
db_name=""

try:
    # define your database connection URL
    database_url = f"mysql+pymysql://{username}:{password}@localhost:3306/{db_name}"
    # create the engine
    engine = create_engine(database_url)
    
    # create a configured "Session" class
    Session = sessionmaker(bind=engine)
    # create a session
    db = Session()
    
    
    inspector = inspect(engine)
    # print(inspector.get_table_names())
    
    records=db.execute(text("""SELECT 
                    COUNT(CASE WHEN age = 26 THEN 1 END) AS younger_count,
                    COUNT(CASE WHEN age <> 26 THEN 1 END) AS older_count,
                    ROUND(COUNT(CASE WHEN age <> 26 THEN 1 END) / COUNT(*) * 100, 2) AS older_percentage
                FROM 
                    test;""")).fetchall()
    
    print(records)
    
except Exception as e:
    print(e)





class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
        
class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("We are on the Home page")
    def post(self):
        # self.write("We are on the Home page post method")
        records=db.execute(text("""SELECT 
                    COUNT(CASE WHEN age = 26 THEN 1 END) AS younger_count,
                    COUNT(CASE WHEN age <> 26 THEN 1 END) AS older_count,
                    ROUND(COUNT(CASE WHEN age <> 26 THEN 1 END) / COUNT(*) * 100, 2) AS older_percentage
                FROM 
                    test;""")).fetchall()    
        return json.dumps({"records":records},default=str)
        
        
class AboutHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("About Us")

class ContactHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Contact Us")
        


async def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([(r"/", MainHandler),
                                           (r"/home", HomeHandler),
                                           (r"/about", AboutHandler),
                                           (r"/contact", ContactHandler),])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    await asyncio.Event().wait()


if __name__ == "__main__":
    
    asyncio.run(main())