"""
Script to create test users in the database with hashed passwords.
Run this once to populate the database with test users.
"""

from app.core.database import get_db, engine
from app.core.security import get_password_hash
from app.models.user import User, UserRole, Profile
from app.models.base import BaseModel


def create_test_users():
    """Create test users in the database."""
    # Create all tables
    BaseModel.metadata.create_all(bind=engine)
    
    # Get database session
    db = next(get_db())
    
    try:
        # Check if users already exist
        existing_admin = db.query(User).filter(User.email == "admin@visiobook.com").first()
        if existing_admin:
            print("✅ Test users already exist in database")
            return
        
        # Create test users with hashed passwords
        test_users = [
            {
                "email": "admin@visiobook.com",
                "username": "admin",
                "password": "admin123",  # Will be hashed
                "role": UserRole.ADMIN,
                "first_name": "Alice",
                "last_name": "Admin",
            },
            {
                "email": "user@visiobook.com",
                "username": "user",
                "password": "user123",  # Will be hashed
                "role": UserRole.USER,
                "first_name": "Bob",
                "last_name": "User",
            },
            {
                "email": "moderator@visiobook.com",
                "username": "moderator",
                "password": "moderator123",  # Will be hashed
                "role": UserRole.MODERATOR,
                "first_name": "Charlie",
                "last_name": "Moderator",
            },
        ]
        
        for user_data in test_users:
            # Create user with hashed password
            password_str = str(user_data["password"])  # Ensure it's a string
            user = User(
                email=user_data["email"],
                username=user_data["username"],
                password=get_password_hash(password_str),  # Hash the password
                role=user_data["role"],
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
            # Create profile for the user
            profile = Profile(
                user_id=user.id,
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
            )
            db.add(profile)
            db.commit()
            
            role_name = user_data["role"].value if hasattr(user_data["role"], 'value') else str(user_data["role"])
            print(f"✅ Created user: {user_data['email']} ({role_name})")
        
        print("\n🎉 Test users created successfully!")
        print("\nYou can now login with:")
        print("  👑 admin@visiobook.com / admin123 (ADMIN)")
        print("  👤 user@visiobook.com / user123 (USER)")
        print("  🛡️  moderator@visiobook.com / moderator123 (MODERATOR)")
        
    except Exception as e:
        print(f"❌ Error creating test users: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_test_users()