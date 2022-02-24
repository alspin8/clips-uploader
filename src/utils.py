import random, json

class GenerationPassword:

    "Génération de mot de passe aléatoire entre 20 et 25 caractères"

    def __rnd(self): return random.choice([random.randint(33,57), random.randint(64,90), random.randint(97,122)]) 

    def __new_generation(self, nb_chars):
        passwd = None
        for i in range(nb_chars):
            passwd += chr(self.__rnd())
        return passwd

    def get_password(self, nb_chars): return self.__new_generation(nb_chars)

class FileUtils:

    @staticmethod
    def get_dict_from_jsonfile(file):
        with open(file) as json_data:
            data_json = json.load(json_data)
        data_str = json.dumps(data_json)
        return json.loads(data_str) 

    @staticmethod
    def write_jsonfile_from_dict(file, dict):
        with open(file, 'w') as json_data:
            return json.dump(dict, json_data)

def date_format(date): return(f"Le {date.replace(date[0:10], f'{date[8:10]}/{date[5:7]}/{date[0:4]}')[0:10]}"
                              f" à {date[12:len(date) - 1]}"
                            )