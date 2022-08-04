# Modules
import requests, json, pprint, re, inquirer, os 
from time import sleep 
from tqdm import tqdm
pp = pprint.PrettyPrinter(indent=4) # makes the output better


# Get env veriable
# TOKEN is your DO Authentication Token
TOKEN = os.getenv('TOKEN') 

def get_key(token):# Function that gets SSH Keys
    key_names = []
    header = {"Authorization": "Bearer %s" % token}
    s = requests.get('https://api.digitalocean.com/v2/account/keys', headers=header)
    keys = s.json()
    for key in keys['ssh_keys']:
        key_names.append({'name': key['name'], 'id': key['id']})
    
    return key_names

def droplet_images():  #This gets the list of droplet images and regions
    image_info = []
    header = {"Content-type": "application/json", "Authorization": "Bearer %s" % TOKEN}
    get = requests.get('https://api.digitalocean.com/v2/images', headers=header)
    images = get.json()['images']
    for image in images:
        image_info.append({'name': image['slug'], 'status': image['status'], 'regions': image['regions']})
    return image_info

def droplet_payload():  # This is the options for our droplet
    question_name = [
        inquirer.Text(name="name", message="Droplet name?,")
    ]
    answer_name = inquirer.prompt(question_name)


    image_options = droplet_images()
    
    Image = question_image = [   #This is the list of all available images in DO
        inquirer.List("image",
        message="Which image?",
        choices=[ image['name'] for image in image_options]
        ),
    ]

    answer_image = inquirer.prompt(question_image)
    for image in image_options:
      if image['name'] == answer_image['image']:
        regions = image['regions']
    
    question_region = [ #This is a list of all available regions in DO
        inquirer.List("region",
        message="Which Region?",
        choices=[ region for region in regions ]
        ),
    ]
    answer_region = inquirer.prompt(question_region)

    
    question_size = [    #This is a list of some of the sizes available in DO
        inquirer.List("size", 
        message="What size?",
        choices=['s-1vcpu-1gb', 's-1vcpu-1gb-amd', 's-1vcpu-1gb-intel', 's-1vcpu-2gb', 's-1vcpu-2gb-amd', 's-1vcpu-2gb-intel',]
        ),
    ]
    answer_size = inquirer.prompt(question_size)

    existing_keys = get_key(token=TOKEN)
    question_sshkey = [ #ssh key ids
        inquirer.List("ssh_keys",
        message="Which key?",
        choices=[ key['name'] for key in existing_keys ]
        ),
    ]
    answer_sshkey = inquirer.prompt(question_sshkey)
    for ssh_key_id in existing_keys: 
        if answer_sshkey['ssh_keys'] == ssh_key_id['name']:
            existing_key_id = ssh_key_id['id']

    print(existing_key_id)


    payload = {
        "name": answer_name['name'],
        "region": answer_region['region'],
        "size": answer_size['size'],
        "image": answer_image['image'],
        "ssh_keys": [
            existing_key_id # SSH Key ID
        ]
    }
    return payload


def get_droplet(id, token):  # This function gets a list of all your droplets in DO
    header = {
        "Authorization": "Bearer %s" % token 
    }
    r = requests.get('https://api.digitalocean.com/v2/droplets/%s'% id, headers=header)
    json_data2 = r.json()
    ip_address = json_data2['droplet']['networks']['v4'][0]['ip_address']

    print("Youre droplet is ready to be connected")
    print("ssh root@%s" % ip_address)

def create_droplet(token, payload): # This function creates a droplet
    header = {
        "Authorization": "Bearer %s" % TOKEN 
        }
    r = requests.post('https://api.digitalocean.com/v2/droplets', data=payload, headers=header)
    json_data = r.json()
    if r.status_code == 200 or 202:
        print(json_data['droplet']['name'] + " is being created")
    else:
        print("There was an error")
        print(json_data['message'])
    for i in tqdm (range (30), desc="Loading..."):
        sleep(1)
        pass
    get_droplet(id=json_data['droplet']['id'], token=TOKEN)

create_droplet(token=TOKEN, payload=droplet_payload())