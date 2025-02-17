import openai
import os
import subprocess

openai.api_key = os.getenv('apikey')

# Generate lambda code
py_response = openai.chat.completions.create(
    model="gpt-4o-mini",  
    messages = [
        { 
            "role": "assistant", 
            "content": "You are a helpful assistant in writing python program." },
        {
            "role": "user",
            "content": "Please write AWS lambda function to read JSON files from an S3 bucket named 'testbucket. Read the contents of these files and count the number of files with 'invoice' in its content. Return only the python code and do not add any instructions in the response.Remove the backticks",
        },
    ],
)

print("printing Python code >>>>\n",py_response.choices[0].message.content);
python_code =  py_response.choices[0].message.content

# Specify the lambda file path
py_path = "src/lambdafunction.py"

# Open the file in write mode and write the content
with open(py_path, "w") as file:
    file.write(python_code)

# Generate SAM template
sam_response = openai.chat.completions.create(
    model="gpt-4o-mini",  
    messages = [
        { 
            "role": "assistant", 
            "content": "You are a helpful assistant in writing AWS templates." },
        {
            "role": "user",
            "content": "Please write a AWS SAM template in YAML to deploy a lambda function from the path './src/lambdafunction.py'. Attach AWS managed policy 'AmazonS3ReadOnlyAccess' to this lambda. Please name the lambda function as 'testlambda_with-ai' and use the runtime 'python3.12'. The lambda should be triggered by API gateway and event path should be 'invoice'. Please make sure this is the only event for the lambda function. Add the lambda ARN alone in the output section of the stack. Return only the YAML code and do not add any instructions in the response. Remove the backticks",
        },
    ],
)

print("printing SAM template >>>>\n", sam_response.choices[0].message.content);
sam_template =  sam_response.choices[0].message.content

# Specify the template file path
sam_path = "template.yml"

# Open the file in write mode and write the content
with open(sam_path, "w") as file:
    file.write(sam_template)

# Define the SAM deploy command with necessary arguments
command = [
    "sam", "deploy", 
    "--stack-name", "simple-stack-with-ai", 
    "--capabilities", "CAPABILITY_IAM",
    "--s3-bucket", "YOUR S3 BUCKET" ### add your S3 bucket here
]

try:
    # Execute the command
    result = subprocess.run(command, check=True, text=True, capture_output=True, shell=True)
    # Print the command's output
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"Error: {e.stderr}")