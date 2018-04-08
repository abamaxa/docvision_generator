# question_factory


##Tests

python -m unittest discover -p "*_test.py"

## Docker

docker build -t question_factory .

docker run -p 4000:80 question_factory --daemon -w 1000 -l 1375 25

docker tag question_factory chrismorgan64/questions:v2.0

docker push chrismorgan64/questions:v2.0
