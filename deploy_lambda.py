import boto3
import argparse
import os
import zipfile
import tempfile
from pathlib import Path

def create_deployment_package():
    """Create a ZIP file containing the Lambda function code"""
    print("Creating deployment package...")
    
    # Create a temporary directory for the package
    with tempfile.TemporaryDirectory() as tmpdir:
        # Copy required files
        files_to_include = [
            'lambda_handler.py',
            'strategy.py',
            'utils.py',
            'database.py',
            'requirements.txt'
        ]
        
        # Create the deployment package
        deployment_package = Path(tmpdir) / 'deployment_package.zip'
        with zipfile.ZipFile(deployment_package, 'w') as zf:
            for file in files_to_include:
                if os.path.exists(file):
                    zf.write(file)
        
        with open(deployment_package, 'rb') as f:
            return f.read()

def deploy_lambda(stack_name, db_password, environment='Production'):
    """Deploy the Lambda function using CloudFormation"""
    cloudformation = boto3.client('cloudformation')
    lambda_client = boto3.client('lambda')
    
    # Read template
    template_path = Path(__file__).parent / 'cloudformation' / 'lambda-template.yaml'
    with open(template_path, 'r') as file:
        template_body = file.read()
    
    try:
        # Create/update stack
        print(f"Deploying stack {stack_name}...")
        cloudformation.create_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Parameters=[
                {
                    'ParameterKey': 'DBPassword',
                    'ParameterValue': db_password
                },
                {
                    'ParameterKey': 'EnvironmentName',
                    'ParameterValue': environment
                }
            ],
            Capabilities=['CAPABILITY_IAM']
        )
        
        # Wait for stack creation
        print("Waiting for stack creation to complete...")
        waiter = cloudformation.get_waiter('stack_create_complete')
        waiter.wait(
            StackName=stack_name,
            WaiterConfig={'Delay': 30, 'MaxAttempts': 60}
        )
        
        # Get function name from stack outputs
        response = cloudformation.describe_stacks(StackName=stack_name)
        outputs = {
            output['OutputKey']: output['OutputValue']
            for output in response['Stacks'][0]['Outputs']
        }
        
        function_name = outputs['LambdaFunctionName']
        
        # Update Lambda function code
        print("Updating Lambda function code...")
        deployment_package = create_deployment_package()
        lambda_client.update_function_code(
            FunctionName=function_name,
            ZipFile=deployment_package
        )
        
        print("\nDeployment completed successfully!")
        print("\nLambda Function Details:")
        print(f"Function Name: {outputs['LambdaFunctionName']}")
        print(f"Function ARN: {outputs['LambdaFunctionArn']}")
        
    except Exception as e:
        print(f"Error deploying Lambda function: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Deploy Bitcoin Trading Bot Lambda Function')
    parser.add_argument('--stack-name', required=True, help='Name of the CloudFormation stack')
    parser.add_argument('--db-password', required=True, help='Database password')
    parser.add_argument('--environment', default='Production', help='Environment name')
    
    args = parser.parse_args()
    deploy_lambda(args.stack_name, args.db_password, args.environment)
