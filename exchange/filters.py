from exchange import app

@app.template_filter()
def dateformat(date, format):
    if not date:
        return None
    return date.strftime(format)

@app.template_filter()
def slash(directory):
    """Adds a slash to a directory because jinja is being a dick about it"""
    return str(directory) + "/"
