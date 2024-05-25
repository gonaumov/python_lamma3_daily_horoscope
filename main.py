import configparser
import os
import re
import subprocess
from datetime import datetime

config_file_name = 'config.ini'


def main():
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    if not os.path.isfile(config_file_name):
        config_file = open(config_file_name, "w", encoding="utf-8")
        config_file.close()

    # Read the configuration file
    config.read(config_file_name)

    user_data = 'USER_DATA'

    # If the section does not exist, create it
    if not config.has_section(user_data):
        config.add_section(user_data)

    user_data_default_items = {
        'date_of_birth': {
            'section_name': 'date_of_birth',
            'section_value': '',
            'section_value_question_part': 'your date of birth'
        },
        'city_of_birth': {
            'section_name': 'city_of_birth',
            'section_value': '',
            'section_value_question_part': 'your city of birth'
        },
        'time_of_birth': {
            'section_name': 'time_of_birth',
            'section_value': '',
            'section_value_question_part': 'your time of birth'
        },
        'country_of_birth': {
            'section_name': 'country_of_birth',
            'section_value': '',
            'section_value_question_part': 'your country of birth'
        }
    }

    user_data_items = {k: set_config_value(config, user_data, v) for k, v in user_data_default_items.items()}

    # Write the updated configuration to the file
    with open(config_file_name, 'w', encoding="utf-8") as configfile:
        config.write(configfile)

    today_date = datetime.today().strftime('%d %B %Y')

    prompt = (f"I was born on {user_data_items['date_of_birth']['section_value']} at "
              f"{user_data_items['time_of_birth']['section_value']} in "
              f"{user_data_items['city_of_birth']['section_value']} "
              f"{user_data_items['country_of_birth']['section_value']}."
              f" Please do for me the most precise horoscope for today {today_date} - according planetary positions "
              f"and etc.")

    command_parameters = ["ollama", "run", "llama3"]

    if os.name == 'nt':
        # 'nt' is the name for Windows
        command_parameters = ["cmd.exe", "/c"] + command_parameters  # Add items at the beginning

    print(prompt)
    print('Creating the daily horoscope for you. Please wait ...')
    result = subprocess.run(command_parameters,
                            input=prompt.encode('utf-8').decode('cp1252'),
                            capture_output=True,
                            text=True)
    print(result.stdout.encode('cp1252').decode('utf-8'))


def set_config_value(config, user_data_section_name, user_data_item):
    if (config.has_option(user_data_section_name, user_data_item["section_name"]) and
            not config.get(user_data_section_name, user_data_item["section_name"]) == "" and
            not re.match(r"\s+", user_data_item["section_name"])):
        # If the option exists, get its value
        user_data_item['section_value'] = config.get(user_data_section_name, user_data_item["section_name"])
    else:
        # If the option does not exist, ask the user for its value
        user_data_item['section_value'] = input(
            f'Please provide value of {user_data_item["section_value_question_part"]}: ').strip()

    config.set(user_data_section_name, user_data_item['section_name'], user_data_item['section_value'].strip())

    return user_data_item


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
