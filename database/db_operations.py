# db_operations.py
from db_init import User, engine
from sqlalchemy.orm import sessionmaker

# Create a Session
Session = sessionmaker(bind=engine)
session = Session()

def create_user(username, email):
  new_user = User(username=username, email=email)
  session.add(new_user)
  session.commit()
  return new_user

def get_user_by_id(user_id):
  return session.query(User).get(user_id)

def update_user_email(user_id, new_email):
  user = session.query(User).get(user_id)
  if user:
    user.email = new_email
    session.commit()
  return user

def delete_user(user_id):
  user = session.query(User).get(user_id)
  if user:
    session.delete(user)
    session.commit()

# Example usage
# if __name__ == "__main__":
#   # Create a new user
#   user = create_user('johndoe', 'john.doe@example.com')
#   print(f"Created new user: {user.username} with ID: {user.id}")

#   # Update the user's email
#   updated_user = update_user_email(user.id, 'new.email@example.com')
#   print(f"Updated user ID {updated_user.id} email to: {updated_user.email}")

#   # Fetch the user by ID
#   fetched_user = get_user_by_id(user.id)
#   print(f"Fetched user ID {fetched_user.id} with email: {fetched_user.email}")

#   # Delete the user
#   delete_user(user.id)
#   print(f"Deleted user ID {user.id}")
