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

## Important Notes

- The deployment uses Python 3.9 on Amazon Linux 2023
- Make sure to use compatible dependencies
- All database credentials are automatically configured in the Elastic Beanstalk environment

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