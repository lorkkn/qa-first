### Test cases for greencity website
### Page link: www.greencity.cx.ua/#/greenCity/events
### Test launch:
```
git clone
python -m venv venv
.\venv\Scripts\activate
source venv/bin/activate
pip install -r requirements.txt
python -m pytest
allure serve allure-results
```
### with this .env
```
BASE_URL=https://www.greencity.cx.ua/#/greenCity/events
BROWSER=chrome
HEADLESS=False
TIMEOUT=10
```
### Author: Matsiuk Oleh
