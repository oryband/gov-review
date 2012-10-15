from annoying.decorators import render_to

@render_to('index.html')
def index(req):
    return {}

@render_to('ministries.html')
def ministries(req):
    return {}

