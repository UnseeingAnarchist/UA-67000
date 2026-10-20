import json

class SettingsManager():
    def __init__(self, bot):
        self.bot = bot
        with open('servers.json', 'r') as servers_file:
            self.servers = json.load(servers_file)
    def add_server_to_dict(self, server_id):
        if server_id not in self.servers:
            self.servers[server_id] = {}
    def log_server(self):
        with open('servers.json', 'w') as servers_file:
            json.dump(self.servers, servers_file, indent=4)
    def change_admin_roll(self, server_id, admin_roll_id):
        self.add_server_to_dict(str(server_id))
        self.servers[server_id]['admin_roll_id'] = admin_roll_id
        self.log_server()
    def set_stalking_consent(self, server_id, value):
        self.add_server_to_dict(str(server_id))
        self.servers[server_id]['stalking_consent_enabled'] = value
        self.log_server()
    def change_stalking_consent_roll(self, server_id, roll_id):
        self.add_server_to_dict(str(server_id))
        self.servers[server_id]['stalking_consent_roll_id'] = roll_id
        self.log_server()
    def set_counting_channel(self, server_id, channel_id):
        self.add_server_to_dict(str(server_id))
        self.servers[server_id]['counting_channel'] = channel_id
        self.log_server()
    
