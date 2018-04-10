# doc_vision_synth


##Tests

python -m unittest discover -p "*_test.py"

## Docker

docker build -t doc_vision_synth .

docker run -p 4000:80 doc_vision_synth --daemon -d 600 -l 600 -w 600 25

docker tag doc_vision_synth chrismorgan64/doc_vision_synth:v2.0

docker push chrismorgan64/doc_vision_synth:v2.0
