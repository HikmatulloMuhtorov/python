import requests, json, pprint #modules
pp = pprint.PrettyPrinter(indent=4) # makes the output better


TOKEN = "example" # your own digital ocean token
header = {
    "Authorization": "Bearer %s" % TOKEN 
    }
payload = {
  "name": "test",
  "region": "nyc3",
  "size": "s-1vcpu-1gb",
  "image": "centos-7-x64",
  "ssh_keys": [
    35624875 # enter your own ssh key id
  ]
}
r = requests.post('https://api.digitalocean.com/v2/droplets', data=payload, headers=header)
pp.pprint(r.json())
