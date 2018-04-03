Run the following commands:
- build the required image: `docker build -t my-redis ./redis`

- run the container: `docker run -p 6379:6379 --name redis my-redis`

In production, nevigate the `redis.conf` file in the `redis` directory and modify variable as needed especially set the **protected-mode** to yes.



## Credits

Thanks for [**Sentdex**](https://github.com/Sentdex) who gave the tutorial about how to use dash and help me build up my very first data visualization app with just some simple work.