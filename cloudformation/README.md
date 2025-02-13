# Bitcoin Trading Bot AWS Deployment

This directory contains AWS CloudFormation templates and scripts for deploying the Bitcoin Trading Bot infrastructure.

## Prerequisites

1. AWS Account with appropriate permissions
2. AWS CLI installed and configured
3. Python 3.11 or later
4. Required Python packages: `boto3`

## Stack Resources

The CloudFormation template creates the following resources:

- VPC with public subnets
- RDS PostgreSQL database
- Elastic Beanstalk environment
- Security groups
- IAM roles and policies
- Environment variables configuration

## Deployment Instructions

1. Configure AWS credentials:
```bash
aws configure
```

2. Deploy the stack:
```bash
python deploy.py --stack-name bitcoin-bot-stack --db-password your-secure-password
```

Optional parameters:
- `--environment`: Environment name (default: Production)

## Post-Deployment

After successful deployment, the script will output:
- Application URL
- Database endpoint
- Database port

## Security Best Practices

1. Use a strong database password
2. Keep AWS credentials secure
3. Regularly rotate credentials
4. Monitor CloudWatch logs
5. Enable SSL/TLS for database connections

## Monitoring and Maintenance

- Monitor application logs in CloudWatch
- Set up CloudWatch alarms for metrics
- Regularly backup the database
- Keep the application updated

## Cleanup

To remove all resources:
```bash
aws cloudformation delete-stack --stack-name bitcoin-bot-stack
```

Note: This will delete all resources including the database. Make sure to backup any important data before deletion.
