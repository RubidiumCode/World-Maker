This is a basic map creation tool, it creates an image using PIL and perlin noise, with plenty of customisation in the main.py file.
A folder called "Saves" will have to be created, as that is where it will try and save the final output.
Some basic performance data is shown below. Being rendered is a 500x500 pixel image with the number of octaves shown in the header column, the times are in seconds.

|Method                                                     |3  |6   |12  |
|-----------------------------------------------------------|---|----|----|
|Python                                                     |68 |132 |260 |
|Python + Rust                                              |131|279 |532 |
|Python + Rust + Mapping                                    |900|1800|3600|
|Python + Memoization (Main Function)                       |70 |133 |267 |
|Python + Rust + Memoization (Main Function)                |132|276 |554 |
|Python + Memoization (All Functions)                       |52 |97  |364 |
|Python + Rust + Memoization (All python Functions          |140|267 |559 |
|Python + Multithreading (20 Threads)                       |41 |84  |258 |
|Python + Multithreading (50 Threads)                       |46 |87  |289 |
|Python + Multithreading (20 Threads) + Memoization (All)   |42 |82  |281 |
|Python + Multithreading (50 Threads) + Memoization (All)   |48 |84  |280 |
