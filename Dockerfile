FROM mongo

#Install git


RUN apt-get update && \
     apt-get install -y git python3.7 python3-pip python3-venv

# RUN pip3 install virtualenv

# RUN /etc/init.d/mongodb start

# mongod --fork --logpath /var/log/mongodb.log
COPY start_mongo.sh /home/ivado/

RUN mkdir -p /home/ivado/ && \      
           cd /home/ivado && \
           git clone  https://github.com/amrnablus/ivado.git

CMD bash /home/ivado/start_mongo.sh 



# RUN cd /home/ivado/ivado && \
#      pip3 install -r requirements.txt

# RUN cd /home/ivado/ivado && \
#      scrapy crawl musmuems

# RUN cd /home/ivado/ivado && \
#      scrapy crawl musmuems

# RUN cd /home/ivado/ivado && \
#      PYTHONPATH=$PYTHONPATH:`pwd` python3 extra_data/city_population.py


# RUN cd /home/ivado/ivado && \
#      PYTHONPATH=$PYTHONPATH:`pwd` python3 ml/linear_regression_influx_pred.py

# #Set working directory
# WORKDIR /home/ivado
