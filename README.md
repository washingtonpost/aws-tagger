# aws-tagger
Tagging AWS resources is hard because each resource type has a different API which is slightly different. The AWS bulk tagging tool eliminates these differences so that you can simplify specify the resource ID and the tags and it takes care of the rest.  Any tags that already exist on the resource will not be removed, but the values will be updated if the tag key already exists. Tags are case sensitive.

## Install
```
pip install aws-tagger
```

## Usage

### Tag individual resource with a single tag
```
aws-tagger --resource i-07a9d0e5 --tag "App:Foobar"  
```

### Tag multiple resources with multiple tags
```
aws-tagger --resource i-07a9d0e5 --resource i-0456e3a9 --tag "App:Foobar" --tag "Team:My Team"
```

### Tag multiple resources from a CSV file
AWS Tagger can also take input from a CSV file. The column names of the CSV file are the tag keys and the colume values are the tag values.
The resource id must be in a column called Id. To switch between regions, you can add a Region column with the standard AWS regions names like us-east-1. If the Region column is missing it assumes that the region is the same as the AWS credentials.
```
echo 'Id,Region,App' > my-resources.csv
echo 'i-11111111,us-east-1,Foobar' >> my-resources.csv
echo 'i-22222222,us-east-1,Foobar' >> my-resources.csv

aws-tagger --csv my-resources.csv
```

## AWS Resource Support
AWS Tagger supports the following AWS resource types. 

### EC2 instances
Any EC2 volumes that are attached to the instance will be automatically tagged.
```
aws-tagger --resource i-07a9d0e5 --tag "App:Foobar"  
```

### S3 buckets
```
aws-tagger --resource my-bucket --tag "App:Foobar"  
```

### RDS instances 
```
aws-tagger --resource arn:aws:rds:us-east-1:111111111:db:my-db --tag "App:Foobar"  

```

### EFS files systems
```
aws-tagger --resource arn:aws:elasticfilesystem:us-east-1:1111111111:file-system/fs-1111111 --tag "App:Foobar"  
```

### Elastic Load Balancers
```
aws-tagger --resource arn:aws:elasticloadbalancing:us-east-1:11111111111:loadbalancer/my-elb --tag "App:Foobar"  
```

### Application Load Balancers
```
aws-tagger --resource arn:aws:elasticloadbalancing:us-east-1:11111111111:loadbalancer/app/nile-content-api-syd-44c45100/f02ac6f33df89ba8 --tag "App:Foobar"  
```

### Elasticache clusters
```
aws-tagger --resource arn:aws:elasticache:us-east-1:111111111:cluster:my-cluster --tag "App:Foobar"  
```

### Elasticsearch clusters 
```
aws-tagger --resource arn:aws:es:us-east-1:111111111:domain/my-domain --tag "App:Foobar"  
```

### Kinesis streams
```
aws-tagger --resource arn:aws:kinesis:us-east-1:111111111:stream/my-stream --tag "App:Foobar"  
```

### Cloudfront distributions
```
aws-tagger --resource arn:aws:cloudfront::1111111111:distribution/E1111111111111 --tag "App:Foobar"  
```

## AWS credentials
AWS Tagger uses the standard AWS credential configuration options. 

### Environment variables
```
export AWS_REGION="us-east-1"
export AWS_ACCESS_KEY_ID="aka..."
export AWS_SECRET_ACCESS_KEY="123..."
aws-tagger --resource i-07a9d0e5 --tag "App:Foobar"  
```

### IAM Roles
AWS Tagger also supports cross-account role assumption. You will still need to configure the initial AWS credentials using one of the methods above, but the role will be used to call the actuall AWS API.

```
aws-tagger --role arn:aws:iam::11111111111:role/MyRole --resource i-07a9d0e5 --tag "App:Foobar"

