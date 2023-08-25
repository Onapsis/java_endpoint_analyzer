class ServletData:
    def __init__(self, filename, app_name, sub_app, entrypoints, auth):
        self.filename = filename
        self.app_name = app_name
        self.sub_app = sub_app
        self.entrypoints = list(entrypoints)
        self.auth = auth

    def filename(self):
        return self.filename
    
    def app_name(self):
        return self.app_name
    
    def sub_app(self):
        return self.sub_app

    def entrypoints(self):
        return self.entrypoints

    def auth(self):
        return self.auth
    