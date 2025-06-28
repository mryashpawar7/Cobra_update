import random
import string
import zlib
import marshal
import types
import os

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))

def obfuscate_code(code_string):
    # First marshal the code object
    code_obj = compile(code_string, '<string>', 'exec')
    marshalled = marshal.dumps(code_obj)
    
    # Compress the marshalled code
    compressed = zlib.compress(marshalled, level=9)
    
    # Convert to bytes representation
    bytes_str = ','.join(str(b) for b in compressed)
    
    # Generate random variable names
    var_names = [generate_random_string() for _ in range(5)]
    
    # Create the loader code with random variables
    loader = f'''import zlib,marshal,types,random,string
{var_names[0]}=[{bytes_str}]
{var_names[1]}=bytes({var_names[0]})
{var_names[2]}=zlib.decompress({var_names[1]})
{var_names[3]}=marshal.loads({var_names[2]})
{var_names[4]}=types.FunctionType({var_names[3]},globals())
{var_names[4]}()
'''
    return loader

def obfuscate_utk():
    input_file = "Extractor/modules/utk.py"
    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found!")
        return
    
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Obfuscate the content
        obfuscated = obfuscate_code(content)
        
        # Generate output filename
        output_file = input_file.replace('.py', '_obfuscated.py')
        
        # Write the obfuscated code
        with open(output_file, 'w') as f:
            f.write(obfuscated)
            
        print(f"✨ Successfully obfuscated utk.py!")
        print(f"📁 Saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🔒 Starting advanced obfuscation for utk.py...")
    obfuscate_utk() 