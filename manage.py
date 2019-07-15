from flask_script import Manager

from mpn import app#, mongo
from mpn.blueprints.user.routes import user_blueprint
from mpn.blueprints.auth.routes import auth_blueprint
from mpn.blueprints.pet.routes import pet_blueprint
from mpn.blueprints.petsit_request.routes import petsit_request_blueprint
from mpn.blueprints.review.routes import review_blueprint
#from mpn.blueprints.payment.routes import payment_blueprint

# register blueprints
app.register_blueprint(user_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(pet_blueprint)
app.register_blueprint(petsit_request_blueprint)
app.register_blueprint(review_blueprint)
#app.register_blueprint(payment_blueprint)

# use app manager to run server and migrate db
manager = Manager(app)

# run application
if __name__ == '__main__':
    app.run(debug=True)
   # manager.run()
