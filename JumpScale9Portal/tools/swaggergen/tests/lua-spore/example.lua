local client = require 'Spore'.new_from_spec('client.json')
resp = client:userscreateWithList_post()
print(resp.status)
print(resp.body)