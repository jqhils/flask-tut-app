from models import *

db.create_all()

new_user = User("funnyname123", "password123")
db.session.add(new_user)
db.session.commit()

user = User.query.get(1)

post1 = Poll(user, "Are you supportive of Donald Trump's free trade initiative?")
db.session.add(post1)
db.session.commit()

post2 = Poll(user, "Is your favourite colour blue?")
db.session.add(post2)
db.session.commit()
