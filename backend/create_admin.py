"""Script to create an admin user for testing."""
import sys
from sqlalchemy.orm import Session

from src.config.database import SessionLocal
from src.models.user import User
from src.utils.password_hasher import password_hasher


def create_admin_user(
    email: str = "admin@example.com",
    password: str = "admin123",
    full_name: str = "Admin User"
) -> None:
    """
    Create an admin user in the database.
    
    Args:
        email: Admin email address
        password: Admin password (will be hashed)
        full_name: Admin full name
    """
    db: Session = SessionLocal()
    
    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.email == email.lower()).first()
        
        if existing_admin:
            print(f"❌ Admin user already exists: {email}")
            print(f"   Role: {existing_admin.role}")
            print(f"   Full Name: {existing_admin.full_name}")
            
            # Ask if user wants to update to admin role
            if existing_admin.role != "admin":
                response = input("\n⚠️  User exists but is not admin. Update to admin role? (yes/no): ")
                if response.lower() in ['yes', 'y']:
                    existing_admin.role = "admin"
                    db.commit()
                    print(f"✅ Updated {email} to admin role")
                else:
                    print("No changes made")
            return
        
        # Create new admin user
        hashed_password = password_hasher.hash_password(password)
        
        admin = User(
            email=email.lower(),
            hashed_password=hashed_password,
            full_name=full_name,
            role="admin"
        )
        
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        print("✅ Admin user created successfully!")
        print(f"   Email: {admin.email}")
        print(f"   Password: {password}")
        print(f"   Role: {admin.role}")
        print(f"   Full Name: {admin.full_name}")
        print(f"\n🔐 You can now login with these credentials")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {str(e)}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("Admin User Creation Script")
    print("=" * 60)
    
    # Allow custom credentials from command line
    if len(sys.argv) > 1:
        email = sys.argv[1]
        password = sys.argv[2] if len(sys.argv) > 2 else "admin123"
        full_name = sys.argv[3] if len(sys.argv) > 3 else "Admin User"
    else:
        email = "admin@example.com"
        password = "admin123"
        full_name = "Admin User"
    
    create_admin_user(email, password, full_name)
    print("=" * 60)
