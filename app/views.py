from app import app, db, models
from flask import jsonify, request

services = [
    {
        'url': u'/api/v1/events',
        'description': u'Gets all events', 
        'HTTP Method': 'GET'
    },
    {
        'url': u'/api/v1/events',
        'description': u'Create a event', 
        'HTTP Method': u'POST',
        'sample body' : u'event : [{"name" : "Morning Ride", "riders" : [{"rider" : "1234", "rider" : "9876", "rider" : "5457"}]}]'
    },
    {
        'url': u'/api/v1/events/{eventId}',
        'description': u'Get and update specific event', 
        'HTTP Method': u'GET/PUT'
    },
    {
        'url': u'/api/v1/events/{groupsId}/riders',
        'description': u'Get all riders for an event', 
        'HTTP Method': u'GET/PUT'
    },
    {
        'url': u'/api/v1/events/{groupsId}/riders/{uniqueId}',
        'description': u'Get and update specific rider', 
        'HTTP Method': u'GET/PUT'
    }
]

BASE_URL = '/api/v1'
@app.route('/')
@app.route('/index')
def index():
	return "RESTful api for skunkworks Bike Trainer app"

@app.route(BASE_URL + '/services', methods=['GET'])
def get_tasks():
    return jsonify({'services': services})

@app.route(BASE_URL + '/events', methods=['GET', 'POST'])
def get_events():
    eventsJSON = []
    events = db.engine.execute("SELECT DISTINCT eventId, eventName FROM events")
    for event in events:
        eventsJSON.append({"name" : event.eventName, "eventId" : event.eventId})

    if request.method == 'POST':
        return jsonify({"post" : "yes"})

    return jsonify({"events" : eventsJSON})

@app.route(BASE_URL + '/events/<int:event_id>', methods=['GET'])
def get_specific_events(event_id):
    eventJSON = {}
    events = db.engine.execute("SELECT DISTINCT eventId, eventName FROM events WHERE eventId = %d" % (event_id))
    for event in events:
        eventJSON['name'] = event.eventName
        eventJSON['eventId'] = event.eventId

    return jsonify({"event" : eventJSON})

@app.route(BASE_URL + '/events/<int:event_id>/riders', methods=['GET', 'PUT'])
def get_riders(event_id):
    eventsJSON = []
    events = db.engine.execute("SELECT * FROM events WHERE eventId = %d" % (event_id))
    for event in events:
        eventsJSON.append({"name" : event.eventName, "eventId" : event.eventId, "riderId" : event.riderId, "speed" : event.speed, "updateTime" : event.updateTime, "createTime" : event.createTime})

    if request.method == 'PUT':
        return jsonify({"put" : "yes"})

    return jsonify({"riders" : eventsJSON})

@app.route(BASE_URL + '/events/<int:event_id>/riders/<rider_id>', methods=['GET', 'PUT'])
def get_specific_rider(event_id, rider_id):
    riderJSON = {}
    riderRequest = request.get_json()

    riders = db.engine.execute("SELECT * FROM events WHERE riderId = \"%s\"" % (rider_id))
    for rider in riders:
        riderJSON['riderId'] = rider.riderId
        riderJSON['createTime'] = rider.createTime
        riderJSON['eventId'] = rider.eventId
        riderJSON['speed'] = rider.speed
        riderJSON['updateTime'] = rider.updateTime
        riderJSON['name'] = rider.eventName

    if request.method == 'PUT':
        ridersJSON = []
        db.engine.execute("UPDATE events SET speed = %f WHERE riderId = \"%s\"" % (riderRequest['speed'], rider_id))
        riders = db.engine.execute("SELECT * FROM events WHERE eventId = %d" % (event_id))
        for rider in riders:
            ridersJSON.append({"name" : rider.eventName, "eventId" : rider.eventId, "riderId" : rider.riderId, "speed" : rider.speed, "updateTime" : rider.updateTime, "createTime" : rider.createTime})

        return jsonify({"riders" :ridersJSON})

    return jsonify({"rider" : riderJSON})
