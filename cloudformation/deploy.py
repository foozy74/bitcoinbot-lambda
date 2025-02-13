import boto3
import argparse
import time

def deploy_stack(stack_name, template_file, parameters):
    """Deploy CloudFormation stack for Bitcoin Trading Bot"""
    cloudformation = boto3.client('cloudformation')
    
    # Read template
    with open(template_file, 'r') as file:
        template_body = file.read()
    
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
    
    deploy_stack(args.stack_name, 'cloudformation/template.yaml', parameters)
