
#!/bin/bash
# brochure-subscription/   ← 📌 Initialize Git repo here!
mkdir app.py .env.example requirements.txt templates static deploy infrastructure .github README.md .gitignore
cd infrastructure
mkdir main.tf variables.tf terraform.tfvars outputs.tf
cd /c/Users/igric/Documents/brochure-subscription/.github
mkdir workflows
cd /c/Users/igric/Documents/brochure-subscription/.github/workflows
touch deploy.yml terraform.yml
