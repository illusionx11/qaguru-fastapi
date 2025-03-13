from faker import Faker

faker = Faker()

def generate_user_data() -> dict[str]:
    email = faker.email(domain="qaguru.autotest")
    first_name = faker.first_name()
    last_name = faker.last_name()
    avatar = f"https://reqres.in/img/faces/{first_name}-{last_name}.jpg"
    
    user_data = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "avatar": avatar
    }
    return user_data