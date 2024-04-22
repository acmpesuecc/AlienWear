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
