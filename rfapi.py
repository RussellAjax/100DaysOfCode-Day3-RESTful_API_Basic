from flask import Flask
from flask_restful import Api, Resource, reqparse
#Importing "Flask", "Api", and "Resource" with capital
#letters initials signifies that a class is being imported
#reqparse is Flask-RESTful request parsing interface
#which will be used later on.

app = Flask(__name__)
api = Api(app)
#Then we create an app using "Flask" class,
#"__name__" is a Python special variable which gives
#Python file a unique name, in this case, we are
#telling the app to run in this specific place.


#Next, we will create a list of users using
#Python data strucutres (lists and dictionaries)
#to simulate a data store
users = [
    {
        "name": "Darren",
        "age": 69,
        "occupation": "Student Council"
    },
    {
        "name": "Steven",
        "age": 420,
        "occupation": "School lowlife"
    },
    {
        "name": "Andrew",
        "age": 0,
        "occupation": "School god"
    }
]
#Note: this method is used since this article is focusing
#in creating API, but in actual condition,
#the data sotre is usually a database.



#Now we will begin creating our API endpoints
#by defining a User resource class.
#Four functions which correspond to four HTTP
#request method will be defined and implemented
#These four methods: get(), post(), put(), delete()
#One of the good quality of a REST API is that it
#follows standard HTTP method to indicate the intended
#action to be performed
class User(Resource):
    def get(self, name):
        #The get() method is used to retrieve a particular
        #user details by specifying the name
        for user in users:
            if(name == user["name"]):
                return user, 200
            return "User not found", 404
        #We will traverse through our users list to search
        #for the user, if the name specified matched with
        #one of the users in users list, we will return
        #the user, along with 200 OF, else return a 404.
        #Another characteristic of a well designed REST 
        #API is that it uses standard HTTP response status
        #code to indicate whether a request is being 
        #processed successfully or not.

    def post(self, name):
        #the post() method is to create a new user
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                return "User with name {} already exists".format(name), 400
            
        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }
        users.append(user)
        return user, 201
        #We will create a parser by using reqparse we 
        #imported earlier, add the age and occupation
        #arguments to the parser, then store the parsed
        #arguments in a variable, args (the argumets will
        #come from request body in the form of
        #form-data, JSON or XML). If a user with same name
        #already exists, the API will return a 400 Bad Request
        #else we will create the user by apending it to users list
        #and return the user along with 201 Created

    def put(self, name):
        #The put method is used to update details of user,
        #or create a new one if it does not exist yet
        perser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                user["age"] = args["age"]
                user["occupation"] = args["occupation"]
                return user, 200
        
        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }
        users.append(user)
        return user, 201
        #if the user already exist, we will update his/her
        #details with the parsed arguments and return the user
        #along with 200 OK, else we will create and 
        #return the user along with 201 Created

    def delete(self, name):
        #The delete method is used to delete the user that 
        #is no longer needed
        global users
        users = [user for user in users if user["name"] != name]
        return "{} is deleted.".format(name), 200
        #By specifying users as a variable in global scope
        #we update the users list using list comprehension
        #to create a list without the name specified (simulating delete)
        #then return a message along with 200 OK


#Finally, we have done implementing all the methods in our
#User resource, we will add the resource to our API and
#specify its route, then run our Flask application:
api.add_resource(User, "/user/<string:name>")
app.run(debug=True)
#Note:
#<stirng:name> indicates that it is a variable part in the
#route which accepts any name. 
#To specify Flask to run in debug mode enables it to reload
#automatically when code is updated and gives us helpful 
#warning messages if something went wrong.
#It is useful in development setting, but should NEVER
#be used in production setting.


