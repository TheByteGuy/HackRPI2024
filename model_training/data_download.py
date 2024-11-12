import requests
import os
import time
from tqdm import tqdm

def janwar_dataset_download_karo(aadhar_url="https://api.inaturalist.org/v1/observations",save_kaha_karna_hai="./dataset/inaturalist"):
    os.makedirs(save_kaha_karna_hai,exist_ok=True)
    apne_param_set_karo={"has[]": "photos","quality_grade": "research","identifications": "most_agree","iconic_taxa[]": ["Animalia","Actinopterygii","Aves","Reptilia","Amphibia","Mammalia","Arachnida","Insecta",],"place_id": 48,"verifiable": "true","popular": "true","per_page": 200}
    uttar=requests.get(aadhar_url,params=apne_param_set_karo,timeout=10)
    if uttar.status_code==200:
        data = uttar.json()
        saare_jawab = data.get("saare_jawab", 0)
        saare_page = (saare_jawab + apne_param_set_karo["per_page"] - 1) // apne_param_set_karo["per_page"]
        print(f"Kitne jawab download karne hai: {saare_jawab} se {saare_page} pages")
    else: 
        print(f"Shuru ka data load karne mein error: {uttar.status_code}")
        return
    while apne_param_set_karo["page"] <= saare_page:
        print(f"\nYe page process ho raha hai {apne_param_set_karo['page']} of {saare_page}")
        uttar = requests.get(aadhar_url, params=apne_param_set_karo, timeout=10)
        if uttar.status_code != 200:
            print(f"Data fetch mein error hai: {uttar.status_code}")
            break
        data = uttar.json()
        uttar = data.get("results", [])
        if not uttar: break
        pbar = tqdm(uttar, desc=f"Downloading page {apne_param_set_karo['page']}")
        for avlokan in pbar:
            if "photos" in avlokan and avlokan["photos"]:
                photo_url = avlokan["photos"][0]["url"]
                taxon_name = avlokan["taxon"]["name"].replace(" ", "_")
                taxon_dir = os.path.join(save_kaha_karna_hai, taxon_name)
                os.makedirs(taxon_dir, exist_ok=True)
                try:
                    img_uttar = requests.get(photo_url, timeout=10)
                    if img_uttar.status_code == 200:
                        img_path = os.path.join(taxon_dir, f"{avlokan['id']}.jpg")
                        with open(img_path, "wb") as f:
                            f.write(img_uttar.content)
                except Exception as e: print(f"Error downloading {photo_url}: {e}")
                time.sleep(0.5)
        apne_param_set_karo["page"] += 1
    print("\nDownload poora hua!")

if __name__ == "__main__":
    janwar_dataset_download_karo()
