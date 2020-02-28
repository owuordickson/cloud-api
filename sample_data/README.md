# How to populate (OGC SensorThings API) database with sample data

Using an integration testing tool (we recommend **Postman** - follow [link](www.postman.com) to download). Initiate the POST requests that follow in the same order that they are listed:

1. Navigate to url: <localhost:8080/v1.0/FeaturesOfInterest>, copy the contents of ```foi.json``` and paste them in the request's body, then send the request. This request will add 1 **FeatureOfInterest** (called *CCIT #361*).

2. Navigate to url: <localhost:8080/v1.0/Things>, copy the contents of ```thing.json``` and paste them in the request's body, then send the request. This request will add 1 **Thing** (called *oven*) which has 3 **Datastreams** (*Temperature, Smoke* and *Motion*). Each **Datastream** has 5 sample **Observations** collected by the respective sensor. NB: make sure the **FeatureOfInterest** ```id``` generated in the previous step is ```1```, otherwise change it to reflect the correct ```id```.
