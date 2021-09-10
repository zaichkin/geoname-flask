# geoname-flask

API для предоставления информации по географическим объектам.

Методы:  
/getbyid/'id'  - Получение информации о городе по его geonameid, где вместо 'id' необходимо указать geonameid города.  
  /getpage/'page'/'number' - Вывод списка городов, где вместо 'page' необходимо указать страницу, а вместо 'number'количество отображаемых городов.  
  /compare/'city1'/'city2' - Метод сравнения двух городов, где вместо 'city1' и 'city2' необходимо указать названия двух городов. Система принимает не строгие названия.  
  /find/'city' - дополнительный метод который выводит подсказку по части названия города, в поле 'city' достаточно ввести пару букв.
