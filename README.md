# Python daily horoscope creator

A pet project which produces daily horoscopes. 
This tiny Python console program creates daily horoscopes for the user by using llama3 model.
You should have ollama installed locally. It asks about user date of birth, time of birth,
city of birth and country of birth and generates horoscope for the current date. User data
is stored in a config file and is required only first time. When the script has the user data 
it doesn't request it anymore. If the config file doesn't exist it will be created. If a user setting
is deleted it will be asked again and updated accordingly. 

## How to use it? 
```python main.py```
