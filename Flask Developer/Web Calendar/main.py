from datetime import datetime
from flask import Flask, abort, request, Response, make_response, jsonify
from flask_restful import inputs, reqparse
from flask_restx import Api, Resource, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
api = Api(app, version='0.0.1', title='EventMVC API', description='A (very) simple EventMVC API')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///name.db'
db = SQLAlchemy(app)
ns = api.namespace('events', )

parser = reqparse.RequestParser()
parser.add_argument('event', type=str, required=True,
                    help="The event name is required!")
parser.add_argument('date', type=inputs.date, required=True,
                    help="The event date with the correct format is required!" +
                         " The correct format is YYYY-MM-DD!")

marshaled_event_fields = {
    "id": fields.Integer,
    "event": fields.String,
    "date": fields.Date,
}


class EventDAO(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.INTEGER, primary_key=True)
    event = db.Column(db.VARCHAR, nullable=False)
    date = db.Column(db.DATE, nullable=False)

    def __repr__(self):
        return "Event(id=" + str(self.id) + \
               ", event='" + str(self.event) + \
               "', date='" + str(self.date) + "')"

    def get_as_dict(self):
        return {"id": int(self.id), "event": str(self.event), "date": str(self.date)}


db.create_all()


class EventTodayRes(Resource):
    @staticmethod
    @ns.marshal_list_with(marshaled_event_fields)
    def get():
        return EventDAO.query.filter(EventDAO.date == datetime.today().date()).all()


class EventByIdRes(Resource):

    @staticmethod
    def get( event_id):
        event = EventDAO.query.filter(EventDAO.id == event_id).first()
        print("Event by ID:", event, ", GET method")
        if event is None:
            print(f"Event by ID: {event_id} is None")
            return make_response({"message": "The event doesn\'t exist!"}, 404, {"mimetype": 'application/json'})
        return make_response(event.get_as_dict(), 200, {"mimetype": 'application/json'})

    @staticmethod
    def delete(event_id):
        event = EventDAO.query.filter(EventDAO.id == event_id).first()
        print("Event by ID:", event, ", DELETE method")
        if event is None:
            return make_response({"message": "The event doesn't exist!"}, 404, {"mimetype": 'application/json'})
        db.session.delete(event)
        db.session.commit()
        return make_response({"message": "The event has been deleted!"}, 200, {"mimetype": 'application/json'})


class EventRes(Resource):
    @staticmethod
    def post():
        args = parser.parse_args()

        db.session.add(EventDAO(event=args.event, date=args.date.date()))
        db.session.commit()

        return {
            "message": "The event has been added!",
            "event": args.event,
            "date": str(args.date.date())
        }

    @ns.marshal_list_with(marshaled_event_fields)
    def get(self):
        args = request.args
        if 'start_time' in args and 'end_time' in args:
            start = args.get('start_time')
            end = args.get('end_time')
            if start and end:
                return EventDAO.query.filter(EventDAO.date.between(start, end)).all()

        return EventDAO.query.all()


api.add_resource(EventTodayRes, "/event/today")
api.add_resource(EventByIdRes, "/event/<int:event_id>")
api.add_resource(EventRes, "/event")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run(port=8000, debug=True)