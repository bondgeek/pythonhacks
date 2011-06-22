#! /usr/bin/env python
'''
testing tornado web server capabilities

'''

import tornado.ioloop
import tornado.web

in_form = """
<html>
 <body>
    <form action="/" method="post">
        <input type="text" name="my_message">
        <input type="submit" value="Click to Submit">
    </form>
 </body>
</html>
"""

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(in_form)
        
    def post(self):
        self.set_header("Content_Type", "text/plain")
        self.write("<h3>Test</h3><p>msg: " + self.get_argument("my_message") + "</p>")

class StoryHandler(tornado.web.RequestHandler):
    def get(self, story_id):
        self.write("You requested the story " + story_id)

application = tornado.web.Application(
            [(r"/", MainHandler),
             (r"/story/([0-9]+)", StoryHandler),
            ],
            debug=True
            )
            
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    