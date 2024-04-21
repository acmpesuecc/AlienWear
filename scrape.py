# import csv
# import requests
# from bs4 import BeautifulSoup

# # def get_background_image_url(url):
# #     response = requests.get(url)
# #     print(f"Response status code for {url}: {response.status_code}")
# #     print(f"Response text for {url}: {response.text[:100]}...") # Print the first 100 characters of the response text
# #     # soup = BeautifulSoup(response.text, 'html.parser')
# #     # image_div = soup.find('div', class_='image-grid-image')
# #     # print(f"Image div for {url}: {image_div}")
# #     # if image_div:
# #     #     style = image_div.get('style')
# #     #     if style:
# #     #         # Extract the URL from the style attribute
# #     #         background_image_url = style.split('url(')[1].split(')')[0]
# #     #         print(f"Background Image URL for {url}: {background_image_url}")
# #     #     else:
# #     #         print(f"No style attribute found for {url}")
# #     # else:
# #     #     print(f"No image div found for {url}")
# #     # return None

# # def scrape_csv_urls(csv_file_path):
# #     # with open(csv_file_path, newline='') as csvfile:
# #     #     reader = csv.DictReader(csvfile)
# #     #     for row in reader:
# #     #         url = row['URL']
# #     url = "https://www.myntra.com/jeans/roadster/roadster-men-navy-blue-slim-fit-mid-rise-clean-look-jeans/2296012/buy"
# #     background_image_url = get_background_image_url(url)
# #     if background_image_url:
# #         print(f"Background Image URL for {url}: {background_image_url}")
# #     else:
# #         print(f"No background image found for {url}")

# # scrape_csv_urls('dataset.csv')

# # url = "https://www.myntra.com/jeans/roadster/roadster-men-navy-blue-slim-fit-mid-rise-clean-look-jeans/2296012/buy"
# url = "https://www.myntra.com"
# response = requests.get(url)
# print(response.text)


# import requests, json
# from bs4 import BeautifulSoup

# headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

# s = requests.Session()
# res = s.get("https://www.myntra.com/jeans/roadster/roadster-men-navy-blue-slim-fit-mid-rise-clean-look-jeans/2296012/buy", headers=headers, verify=False)

# soup = BeautifulSoup(res.text,"lxml")

# script = None
# for s in soup.find_all("script"):
#     if 'pdpData' in s.text:
#         script = s.get_text(strip=True)
#         break

# print(json.loads(script[script.index('{'):]))

# import requests
# import json
# from bs4 import BeautifulSoup

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
# }

# s = requests.Session()
# res = s.get("https://www.myntra.com/jeans/roadster/roadster-men-navy-blue-slim-fit-mid-rise-clean-look-jeans/2296012/buy", headers=headers, verify=False)

# soup = BeautifulSoup(res.text, "lxml")

# script = None
# for s in soup.find_all("script"):
#     if 'pdpData' in s.text:
#         script = s.get_text(strip=True)
#         break

# json_data = json.loads(script[script.index('{'):])

# image_link=json_data["pdpData"]["media"]["albums"][0]["images"][0]["imageURL"]


import pandas as pd
import requests
import json
from bs4 import BeautifulSoup

# Function to extract image link from URL
def get_image_link(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    try:
        res = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(res.text, "lxml")
        script = None
        for s in soup.find_all("script"):
            if 'pdpData' in s.text:
                script = s.get_text(strip=True)
                break
        json_data = json.loads(script[script.index('{'):])
        image_link = json_data["pdpData"]["media"]["albums"][0]["images"][0]["imageURL"]
        return image_link
    except Exception as e:
        print(f"Error fetching image for URL {url}: {e}")
        return None

# Read CSV file into DataFrame
df = pd.read_csv("fashionOG.csv")

# Apply function to each row to fetch image link
df['ImageLink'] = df['URL'].apply(get_image_link)

# Save the updated DataFrame with image links
df.to_csv("updated_dataset_with_images.csv", index=False)
