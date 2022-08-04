import requests, json, pprint, re, inquirer, os #modules
pp = pprint.PrettyPrinter(indent=4) # makes the output better


# Get env veriable
TOKEN = os.getenv('TOKEN') #TOKEN is your DO Authentication Token

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

    
    Size = question_size = [    #This is a list of some of the sizes available in DO
        inquirer.List("size", 
        message="What size?",
        choices=['s-1vcpu-1gb', 's-1vcpu-1gb-amd', 's-1vcpu-1gb-intel', 's-1vcpu-2gb', 's-1vcpu-2gb-amd', 's-1vcpu-2gb-intel',]
        ),
    ]
    answer_size = inquirer.prompt(question_size)

    payload = {
        "name": answer_name['name'],
        "region": answer_region['region'],
        "size": answer_size['size'],
        "image": answer_image['image'],
        "ssh_keys": [
            35804415 # enter your own ssh key id
        ]
    }
    return payload


def create_droplet(token, payload): # This function creates a droplet
    header = {
        "Authorization": "Bearer %s" % TOKEN 
        }
    r = requests.post('https://api.digitalocean.com/v2/droplets', data=payload, headers=header)
    return r.json()


def get_droplet(token):  # This function gets a list of all your droplets in DO
    header = {
        "Authorization": "Bearer %s" % token 
    }
    r = requests.get('https://api.digitalocean.com/v2/droplets', headers=header)
    return r.json()


create_droplet(token=TOKEN, payload=droplet_payload())