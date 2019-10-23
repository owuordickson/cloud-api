# Gradual Pattern Mining Tools (GRAANK)
This application is served by uWSGI:NGINX server and it receives HTTP POST requests from the Data Analysis Service and it returns responses with the patterns extracted. Each request contains a JSON body with selected algorithm and the data streams from which gradual patterns are to be extracted.

### Usage
Below is a sample of how the JSON body of the request should look like:

'''

{
    "patternType": "gradual",
    "minSup": 0.5,
    "steps": 20,
    "combs": 100,
    "m_rep": 0.5,
    "c_ref": 0,
    "crossingList": [
        {
            "id": 12,
            "name": "air humidity",
            "observations": [
                {
                    "time": "2013-04-18T23:15:19.000Z",
                    "value": 4
                },
                {
                    "time": "2013-04-18T23:15:15.000Z",
                    "value": 3
                }
            ]
        },
        {
            "id": 11,
            "name": "oven temperature",
            "observations": [
                {
                    "time": "2013-04-18T23:15:20.000Z",
                    "value": 105
                },
                {
                    "time": "2013-04-18T23:15:15.000Z",
                    "value": 110
                }
            ]
        }
    ]
}

'''
