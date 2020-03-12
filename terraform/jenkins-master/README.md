# This project is using terraform workspaces. This is needed to keep state files separate , and to create unique naming resources with same terraform code

Example to create Jenkins server for dev:

```bash
terraform init
terraform workspace select dev || terraform workspace new dev
terraform plan
terraform apply
```
