from mongoengine import *
import datetime

from mpn.config import MONGO_DBNAME, MONGO_URI

connect(MONGO_DBNAME, host=MONGO_URI)

class User(Document):

    # meta
    created_timestamp = DateTimeField(required=True, default=datetime.datetime.utcnow)
    updated_timestamp = DateTimeField(required=True, default=datetime.datetime.utcnow)

    # profile info
    name = StringField(required=True, max_length=50)
    email_address = EmailField(required=True, unique=True)
    password_hashed = StringField(required=True)
    profile_img = StringField(required=True, default="default.jpg")

    # points
    petsit_points = IntField(required=True, default=100)
    birth_date = DateTimeField()
    stripe_id = StringField() 

    # about residence
    address = StringField(required=True)
    city = StringField(required=True)
    state = StringField(required=True)
    postal_code = StringField(required=True)
    coordinates = PointField(required=True)
    #residence_type = StringField("Condo", "Apartment")
        


class PetSitAvailability(Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE)

    available = IntField(default=1)

    # Availalble (1), Not Available (0), Maybe Available (2)
    monday_day = IntField(default=1) 
    monday_night = IntField(default=2) 
    tuesday_day = IntField(default=1) 
    tuesday_night = IntField(default=2) 
    wednesday_day = IntField(default=1) 
    wednesday_night = IntField(default=2) 
    thursday_day = IntField(default=1) 
    thursday_night = IntField(default=2) 
    friiday_day = IntField(default=1) 
    friiday_night = IntField(default=2) 
    saturday_day = IntField(default=1) 
    saturday_night = IntField(default=2) 
    sunday_day = IntField(default=1) 
    sunday_night = IntField(default=2) 

class Pet(Document):
    created_timestamp = DateTimeField(required=True, default=datetime.datetime.utcnow)
    updated_timestamp = DateTimeField(required=True, default=datetime.datetime.utcnow)

    name = StringField(required=True)
    owner = ReferenceField(User, reverse_delete_rule=CASCADE)
    birth_date = DateTimeField()
    birth_year = IntField()
    gender = StringField()
    profile_img = StringField(required=True, default="default.jpg")
    # *** SPECIAL CONDITIONS ***

    meta = {'allow_inheritance': True}

    # http://docs.mongoengine.org/guide/document-instances.html#pre-save-data-validation-and-cleaning
    # https://stackoverflow.com/a/18790842
    def clean(self):

        # write a validation method for none duplicate pet under the same user
        pass


class Dog(Pet):
    potty_trained = IntField()  # Yes (1), No (0), Sometimes (2)
    neutered = IntField()  # Yes (1), No (0)
    aggression_level = IntField()
    breed = StringField()
    weight_lb = DecimalField() 


class Review(Document):
    created_timestamp = DateTimeField(required=True, default=datetime.datetime.utcnow)
    updated_timestamp = DateTimeField(required=True, default=datetime.datetime.utcnow)
    reviewer = ReferenceField(User, required=True, reverse_delete_rule=CASCADE)
    rating = IntField(required=True, min_value=1, max_value=5)
    comment = StringField()
    meta = {'allow_inheritance': True}
    
class PetReview(Review):
    pet = ReferenceField(Pet, required=True)

class UserReview(Review):
    user = ReferenceField(User, required=True)


class PetSitRequestSlot(EmbeddedDocument):
    start_datetime = DateTimeField(required=True)
    end_datetime = DateTimeField(required=True)

class PetSitRequest(Document):
    created_timestamp = DateTimeField(required=True, default=datetime.datetime.utcnow)
    updated_timestamp = DateTimeField(required=True, default=datetime.datetime.utcnow)

    requester = ReferenceField(User, required=True)
    recipient = ReferenceField(User, required=True)
    
    points_offered = IntField(required=True)
    request_message = StringField()
    request_slots = ListField(EmbeddedDocumentField(PetSitRequestSlot), required=True)

    response = IntField()  # 1 for accepted, 0 for denied
    response_reason = StringField()
    response_message = StringField()

    fulfillment_status = IntField()  # 1 for fulfilled, 0 for not fulfilled, 2 for problem



class Payment(Document):
    created_timestamp = DateTimeField(required=True, default=datetime.datetime.utcnow)
    updated_timestamp = DateTimeField(required=True, default=datetime.datetime.utcnow)
    user = ReferenceField(User, required=True)
    amount = DecimalField(required=True) 
    received_points = IntField(required=True) 