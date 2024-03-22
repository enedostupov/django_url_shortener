# This implementation consists of
1. Django and django rest framework for processing incoming requests via REST
2. Celery and Redis to perform background asynchronous tasks
3. PostgreSQL as the main repository

# Spin up the containers:
```sh
$ docker-compose up -d --build
```
If you get an error, you may need to run ```$ chmod +x entrypoint.sh```

# End-points and usage examples:
1. **Reduce url**

   **POST** /shortener/

   **example**
   ``` 
   curl -X POST http://127.0.0.1:1337/shortener/ -H "Content-Type: application/json" -d '{"url": "http://ya.ru"}'
   ```
   **response**
   ```
   {
        'short_url': 'http://127.0.0.1:1337/shortener/z'
   }
   ```

2. **Get the original url by short**

   **GET** /shortener/<shorten_url>
   
   **example** 
   ```
   curl http://127.0.0.1:1337/shortener/z
   ```
   **response**
   ```
   {
        'original_url': 'http://vk.com'
   }
   ```

3. **Get top100 URLs**
   
   **GET** /shortener/top/
   
   **example** 
   ```
   curl http://127.0.0.1:1337/shortener/top/
   ```
   **response**
   ```
   [
        {"original_url":"http://gmail.com","count":3,"title":"Gmail"},
        {"original_url":"http://vk.com","count":1,"title":"VK.com | VK"},
        {"original_url":"http://google.com","count":0,"title":"Google"},
        {"original_url":"http://yahoo.com","count":0,"title":"Yahoo | Mail, Weather, Search, Politics, News, Finance, Sports & Videos"},
    ]
    ```

# Short url generation:
The process of creating short URLs involves using a counter that is safe for concurrent access. With each request to generate a short URL, this counter is increased by one. The incremented value is then translated into a base 37 numbering system, which includes both digits (0-9) and letters (a-z). The counter's modification is securely managed within a transaction that applies record locking, ensuring its safety for use in multithreaded scenarios. This makes the counter robust and suitable for distributed applications, where multiple processes or service instances handle incoming requests simultaneously.

# Benefits:
1. Guarantees the generation of the shortest possible URL.
2. Utilizes Docker Compose for streamlined deployment and configuration.
3. Includes comprehensive test coverage to ensure reliability.
 
# Areas for Enhancement and Proposed Solutions:
0. Storing user password and secret keys information in settings and Docker Compose files is not secure. It's essential to relocate this information to a more secure environment.
1. Caching Absence at /shortener/ Endpoint:
   Solution: Implementing a caching layer, such as Redis, could significantly enhance performance. This layer would first attempt to retrieve the short URL from the cache before defaulting to a PostgreSQL query if not found. Additionally, incorporating a background process to increment the query count would optimize efficiency further.
2. Caching Absence at /shortener/top Endpoint:
   Current Challenge: Currently, each request triggers an aggregate query across the entire table containing URLs, which can be resource-intensive.
   Proposed Improvement: If feasible, relocating the storage of the top 100 URLs to Redis could alleviate strain on the system. This cache would only need refreshing at intervals, perhaps every 5-10 minutes, through a comprehensive table query, thus reducing the load on the database.
