# Automatic AWS MFA Login

Tired of restarting docker containers that need AWS MFA access every 15 minutes?
With `aws_login_reload` you can set your OTP secret in an environment variable and let it reload the docker container automatically.

### setting up

```bash
git clone git@github.com:samuelantonioli/aws-mfa-reload.git && cd aws-mfa-reload
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
echo "$(pwd)/env/bin/python3 aws_login_reload.py" > run.sh && chmod +x run.sh
```
### running

```bash
export OTP_SECRET="otpauth-migration://offline?data=SECRET_DATA"
export AWS_PROFILE=aws-profile-name
export DOCKER_CONTAINER=docker-container-name
./run.sh
```

