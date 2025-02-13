import boto3
import argparse
import time
import os
from pathlib import Path

def deploy_stack(stack_name, template_file, parameters):
    """Deploy CloudFormation stack for Bitcoin Trading Bot"""
    cloudformation = boto3.client('cloudformation')

    # Get absolute path to template file
    template_path = Path(__file__).parent / template_file

    # Read template
    try:
        with open(template_path, 'r') as file:
            template_body = file.read()
    except FileNotFoundError:
        print(f"Error: Template file not found at {template_path}")
        print("Make sure you're running the script from the project root directory")
        return

    try:
        # Create stack
        print(f"Creating stack {stack_name}...")
        cloudformation.create_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Parameters=[
                {
                    'ParameterKey': 'DBPassword',
                    'ParameterValue': parameters['db_password']
                },
                {
                    'ParameterKey': 'EnvironmentName',
                    'ParameterValue': parameters['environment']
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

        # Get stack outputs
        response = cloudformation.describe_stacks(StackName=stack_name)
        outputs = response['Stacks'][0]['Outputs']

        print("\nDeployment completed successfully!")
        print("\nApplication Details:")
        for output in outputs:
            print(f"{output['Description']}: {output['Value']}")

    except Exception as e:
        print(f"Error deploying stack: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Deploy Bitcoin Trading Bot to AWS')
    parser.add_argument('--stack-name', required=True, help='Name of the CloudFormation stack')
    parser.add_argument('--db-password', required=True, help='Database password')
    parser.add_argument('--environment', default='Production', help='Environment name')

    args = parser.parse_args()

    parameters = {
        'db_password': args.db_password,
        'environment': args.environment
    }

    # Use relative path from script location
    template_file = 'template.yaml'
    deploy_stack(args.stack_name, template_file, parameters)