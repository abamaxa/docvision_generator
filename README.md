# question_factory


docker build -t question_factory .

docker run -p 4000:80 question_factory --daemon -w 1000 -l 1375 25

docker push chrismorgan64/questions:v1.1
