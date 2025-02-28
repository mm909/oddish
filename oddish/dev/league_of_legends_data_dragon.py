import os
import time
import tarfile
import json
import requests
from requests.exceptions import RequestException
from tqdm import tqdm

from colorthief import ColorThief

from league_of_legends_data_dragon_config import default_config

class LeagueOfLegendsDataDragon:

    def __init__(self, config=None):
        self.config = config or default_config

        self.DATA_DRAGON_URL = 'https://ddragon.leagueoflegends.com/'

        # Versions
        self.dd_versions = self.query_data_dragon_versions()
        self.current_version = self.dd_versions[0]
        print(f'Current version: {self.current_version}')

        # self.download_data_dragon_tgz(self.current_version)
        # self.extract_data_dragon_tgz(self.current_version)
        self.get_data()
        return 


    def get_data(self):
        self.get_champion_list()
        self.get_skill_list()
        self.get_primary_colors_from_spells()
        return
    

    def get_champion_list(self):
        self.champion_data = {}
        with open(f'{self.config["output_folder"]}/dragontail/data/{self.current_version}/data/en_US/championFull.json', 'r', encoding='utf-8') as f:
            self.champion_data = json.load(f)
        self.champion_list = list(self.champion_data['data'].keys())
        self.champion_data = self.champion_data['data']
        # print(f'Champion data: {self.champion_data}')
        # print(f'Champion list: {self.champion_list}')
        return self.champion_list
    

    def get_skill_list(self):
        spell_list = {}
        spell_order = ['Q', 'W', 'E', 'R']
        for champion in self.champion_data:
            champ_spells = {}
            for index, spell in enumerate(self.champion_data[champion]['spells']):
                champ_spells[spell_order[index]] = spell['id']
            passive = self.champion_data[champion]['passive']
            champ_spells['P'] = passive['image']['full'].replace('.png', '')
            spell_list[champion] = champ_spells
    
        self.spell_list = spell_list    



    def get_primary_colors_from_spells(self):
        output_folder = f'{self.config["output_folder"]}/dragontail/data/{self.current_version}/img/'
        self.spell_colors = {}
        for champion in self.spell_list:
            print(f'Getting primary color for {champion}')
            for spell in self.spell_list[champion]:
                spell_id = self.spell_list[champion][spell]
                if spell == 'P':
                    url = f'{output_folder}passive/{spell_id}.png'
                else:
                    url = f'{output_folder}spell/{spell_id}.png'

                color_thief = ColorThief(url)
                dominant_colors = color_thief.get_color(quality=1)
                self.spell_colors[f'{champion}_{spell}'] = dominant_colors



    def query_data_dragon_versions(self):
        try:
            response = requests.get(f'{self.DATA_DRAGON_URL}/api/versions.json', timeout=10)
            response.raise_for_status()
            versions = response.json()
            return versions
        except RequestException as e:
            print(f'Error: {e}')
            return None
        
    
    def download_data_dragon_tgz(self, version=None):
        if version is None:
            version = self.current_version

        ts = time.time()
        url = f'{self.DATA_DRAGON_URL}/cdn/dragontail-{version}.tgz'
        folder = f'{self.config["output_folder"]}/dragontail'
        file_path = f'{folder}/dragontail-{version}.tgz'

        if os.path.exists(file_path):
            return file_path

        print(f'Downloading {url}')
        try:
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()

            os.makedirs(folder, exist_ok=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kilobyte

            with open(file_path, 'wb') as f, tqdm(
                total=total_size, unit='iB', unit_scale=True
            ) as bar:
                for data in response.iter_content(block_size):
                    bar.update(len(data))
                    f.write(data)

            print(f'Download complete: {file_path} in {time.time() - ts:.2f} seconds')
            return file_path
        except RequestException as e:
            print(f'Error: {e}')
            return None


    def extract_data_dragon_tgz(self, version=None):
        if version is None:
            version = self.current_version

        file_path = self.download_data_dragon_tgz(version)
        if file_path is None:
            return None

        ts = time.time()
        print(f'Loading {file_path}')
        try:
            with tarfile.open(file_path, 'r:gz') as tar:
                def is_within_directory(directory, target):
                    
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)
                
                    prefix = os.path.commonprefix([abs_directory, abs_target])
                    
                    return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                    for member in tar.getmembers():
                        member_path = os.path.join(path, member.name)
                        if not is_within_directory(path, member_path):
                            raise Exception("Attempted Path Traversal in Tar File")
                
                    tar.extractall(path, members, numeric_owner=numeric_owner) 
                    
                
                safe_extract(tar, path=f'{self.config["output_folder"]}/dragontail/data/')
            print(f'Load complete: {file_path} in {time.time() - ts:.2f} seconds')
            return True
        except Exception as e:
            print(f'Error: {e}')
            return False
        


if __name__ == '__main__':
    lol = LeagueOfLegendsDataDragon()