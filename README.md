# Running the project
To create a docker container, run the following command: 
```bash
curl  https://raw.githubusercontent.com/amrnablus/ivado/master/DockerFile | docker build - --build-arg MONGO_HOST=<mongo_host>

```
(i didn't get enough time to add mongo as a dependency, it needs to be added separately)

The docker file will create a docker container and execute the requirements, the image can be accessed and checked for the results in the directory: `/home/ivado`

# Tech stack:
* Codebase: Python
* Scrapy for collecting wikipedia data
* wikidata with fail over to opendatasoft for city population

# Notes:
* Due to the textual nature of the data, not all the cities were mapped correctly and thus, not all the population data was acquired correctly.
* As a fix to the previous point, i added some special cases in the code, however, if i'm to present this to the client i'd recommend they fill up the missing data manually rather than having a code full with special cases that occur only once
* I chose mongodb for metadata storage, the reason for that is the dynamic nature of the metadata of museums makes a document storage most appropriate
* The logistic regression code has a very low accuracy and should not be used in production, there is no simple corelation between the population of a city and the number of visitors, i would recommend adding more features such as the number of tourists visiting the city, the cost of entering the museum, in the case this isn't enough, some other features can be thought of such as the weather in that particular city and the proximity to other entertainment centres
 