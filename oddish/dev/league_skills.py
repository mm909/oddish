import os
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import random

from colorthief import ColorThief


class LeagueData:
    def __init__(self):

        # self.get_data()
        # self.save_cdn_data()

        self.load_data()
        self.build_example_graph()


    def build_example_graph(self):
        # Number of iterations to select a new random champion each time
        num_iterations = 10

        # Calculate the number of rows and columns
        num_cols = 5
        num_rows = num_iterations

        # Create a figure with multiple rows
        fig, axs = plt.subplots(num_rows, num_cols, figsize=(20, 4 * num_rows))
        axs = axs.flatten()  # Flatten the 2D array of axes for easy indexing

        for i in range(num_iterations):
            # Select a random champion
            champion = random.choice(self.champion_list)

            imposter_kit = self.get_imposter_kit(champion)

            for index, spell in enumerate(imposter_kit):
                skill = imposter_kit[spell]
                current_champ = skill.split('_')[0]
                spell = skill.split('_')[1]

                folder_path = f'images/spells/{current_champ}/'
                img = plt.imread(f'{folder_path}/{skill}.png')
                axs[i * num_cols + index].imshow(img)
                axs[i * num_cols + index].axis('off')
                # axs[i * num_cols + index].set_title(f'{current_champ} {spell}')

        # Hide any unused subplots
        for ax in axs[num_iterations * num_cols:]:
            ax.axis('off')

        plt.show()

            

    def get_imposter_kit(self, champion):
        imposter_spells = self.get_imposter_spells(champion)

        imposter_kit = {
            'P': f'{champion}_P',
            'Q': f'{champion}_Q',
            'W': f'{champion}_W',
            'E': f'{champion}_E',
            'R': f'{champion}_R',
        }
        imposter_kit[imposter_spells['replaced_spell'].split('_')[1]] = imposter_spells['selected_spell']

        return imposter_kit



    
    def get_imposter_spells(self, champion):
        distance_table_df = pd.DataFrame(self.distance_table)

        selected_cols = [col for col in distance_table_df.columns if col.startswith(champion)]
        distance_table_df = distance_table_df[selected_cols]
        distance_table_df = distance_table_df.drop(selected_cols, axis=0)

        distance_table_df['sum'] = distance_table_df.sum(axis=1)
        distance_table_df = distance_table_df.sort_values(by='sum')

        n = 20
        top_n = distance_table_df.head(n)

        # select a row w/ probability based on distance
        top_n = top_n.copy()  # Ensure we are working on a copy
        top_n.loc[:, 'probability'] = top_n['sum'] / top_n['sum'].sum()

        selected_spell = top_n.sample(weights=top_n['probability'])
        selected_spell_name = selected_spell.index[0]

        replaced_spell = selected_spell[selected_cols].idxmax(axis=1).iloc[0]
        print(f'{champion} will replace {replaced_spell} with {selected_spell_name}')

        return {
            'selected_spell': selected_spell_name,
            'replaced_spell': replaced_spell,
        }



    def build_distance_table_between_spell_colors(self):
        self.distance_table = {}
        for spell1 in self.spell_colors:
            self.distance_table[spell1] = {}
            for spell2 in self.spell_colors:
                distance = self.get_distance_between_colors(self.spell_colors[spell1], self.spell_colors[spell2])
                self.distance_table[spell1][spell2] = distance

        
    def get_distance_between_colors(self, color1, color2):
        r1, g1, b1 = color1
        r2, g2, b2 = color2

        distance = ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
        return distance



    def get_primary_colors_from_spells(self):
        output_folder = 'images/spells/'
        self.spell_colors = {}
        for champion in self.spell_list:
            print(f'Getting primary color for {champion}')
            for spell in self.spell_list[champion]:
                folder_path = f'{output_folder}{champion}/'

                color_thief = ColorThief(f'{folder_path}/{champion}_{spell}.png')
                dominant_colors = color_thief.get_color(quality=1)
                self.spell_colors[f'{champion}_{spell}'] = dominant_colors

        with open('spell_colors.json', 'w') as f:
            json.dump(self.spell_colors, f)


    def get_spell_images(self):
        output_folder = 'images/spells/'
        for champion in self.spell_list:
            print(f'Getting images for {champion}')
            for spell in self.spell_list[champion]:
                spell_id = self.spell_list[champion][spell]
                if spell == 'P':
                    url = f'https://ddragon.leagueoflegends.com/cdn/{self.version}/img/passive/{spell_id}.png'
                else:
                    url = f'https://ddragon.leagueoflegends.com/cdn/{self.version}/img/spell/{spell_id}.png'
                data = requests.get(url)

                folder_path = f'{output_folder}{champion}/'
                os.makedirs(folder_path, exist_ok=True)
                with open(f'{folder_path}/{champion}_{spell}.png', 'wb') as f:
                    f.write(data.content)


    def get_spell_list(self):
        spell_list = {}
        spell_order = ['Q', 'W', 'E', 'R']
        for champion in self.champion_data:
            champ_spells = {}
            for index, spell in enumerate(self.champion_data[champion]['data'][champion]['spells']):
                champ_spells[spell_order[index]] = spell['id']
            passive = self.champion_data[champion]['data'][champion]['passive']
            champ_spells['P'] = passive['image']['full'].replace('.png', '')
            spell_list[champion] = champ_spells
    
        self.spell_list = spell_list            
        

    def load_data(self):
        with open('version.json', 'r') as f:
            self.version = json.load(f)['version']

        with open('champion_meta_data.json', 'r') as f:
            self.champion_meta_data = json.load(f)

        with open('champion_data.json', 'r') as f:
            self.champion_data = json.load(f)

        self.get_champion_list()

        with open('spell_list.json', 'r') as f:
            self.spell_list = json.load(f)

        with open('spell_colors.json', 'r') as f:
            self.spell_colors = json.load(f)

        with open('distance_table.json', 'r') as f:
            self.distance_table = json.load(f)


    def get_lol_version(self):
        data = requests.get('https://ddragon.leagueoflegends.com/api/versions.json')
        version = json.loads(data.text)[0]
        return version


    def get_champion_meta_data(self):
        data = requests.get(f'https://ddragon.leagueoflegends.com/cdn/{self.version}/data/en_US/champion.json')
        champion_data = json.loads(data.text)
        return champion_data


    def get_champion_list(self):
        self.champion_list = []
        for champion in self.champion_meta_data['data']:
            self.champion_list.append(champion)
        return self.champion_list


    def get_champion_data(self):
        self.champion_data = {}
        for champion_name in self.champion_list:
            print(f'Loading data for {champion_name}')
            data = requests.get(f'https://ddragon.leagueoflegends.com/cdn/{self.version}/data/en_US/champion/{champion_name}.json')
            champion_data_loaded = json.loads(data.text)
            self.champion_data[champion_name] = champion_data_loaded
        return 
    

    def get_data(self):
        self.version = self.get_lol_version()
        print(f'Version: {self.version}')

        self.champion_meta_data = self.get_champion_meta_data()
        self.champion_list = self.get_champion_list()
        print(f'{len(self.champion_list)} champions found')

        self.get_champion_data()
        print(f'Champion data loaded')

        self.get_spell_list()
        self.get_spell_images()
        self.get_primary_colors_from_spells()
        self.build_distance_table_between_spell_colors()



    def save_cdn_data(self):
        with open('version.json', 'w') as f:
            json.dump({'version': self.version}, f)

        with open('champion_meta_data.json', 'w') as f:
            json.dump(self.champion_meta_data, f)

        with open('champion_data.json', 'w') as f:
            json.dump(self.champion_data, f)

        with open('spell_list.json', 'w') as f:
            json.dump(self.spell_list, f)

        with open('spell_colors.json', 'w') as f:
            json.dump(self.spell_colors, f)

        # with open('distance_table.json', 'w') as f:
        #     json.dump(distance_table, f)


        return


if __name__ == '__main__':
    league_data = LeagueData()
