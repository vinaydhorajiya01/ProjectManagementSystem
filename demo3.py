import re
from datetime import datetime

string = "https://storage.googleapis.com/projectmanagement-3e8a8.appspot.com/DESKTOP-3S7MM6C/1680693760.2837706.png?Expires=1680946276&GoogleAccessId=firebase-adminsdk-zjxws%40projectmanagement-3e8a8.iam.gserviceaccount.com&Signature=fn1SmPoANKHOiioOVskPYwyoeR1TF%2BSikJODFYKnpLoTBOdscdxchbQQBi655M8X6sf3jPDGL%2FVKcDWsg6O9GGjzyoxh%2FiNsJobDAXFKg3uWBAKkqrrw0zOAxbNfxwbD5XjlJauEAmt0doG%2BAeYj6nqUAym87phjOGxT7sxgGlmNMXaoegVyK0c0qnqzgKOlx6tejMuwAPg8Ad1wwT4iYXbkyRg5Q%2FAfBNd1J13ojaMchCxqGqqdmpXr0Z9%2FdzNkO2zSlde30Lw5GlHVnlMubPaQ7pN5%2Fpj6bvKcVDCfknc85zRqJpOMsm3vea8farN7eCV6i5W8i3FfFn8fu3pC7w%3D%3D"


pattern = r'/(\d+\.\d+)\.'
print(re.match(pattern, string))
list = re.findall(pattern, string)
date = float(list[0])
date = datetime.fromtimestamp(date)
print(date.time())
print(date.date())