"""
pip install pyotp protobuf pexpect

Set your secret via
export OTP_SECRET="otpauth-migration://offline?data=SECRET_DATA"
And AWS profile from config
export AWS_PROFILE=aws-profile
export DOCKER_CONTAINER=your-docker-container-name
"""
import subprocess
import os
import time
import pexpect
from decode_otp import decode


def get_otp_code():
    otp_secret = os.getenv("OTP_SECRET")
    return decode(otp_secret)


def start_command_with_input(command, input_data):
    child = pexpect.spawn(command)
    try:
        i = child.expect([pexpect.TIMEOUT, "Enter MFA code"])
    except pexpect.exceptions.EOF:
        # still logged in
        print(child.before.decode("utf-8"))
        return "assumed-role" in child.before.decode("utf-8"), False
    child.sendline(input_data)
    print(child.read().decode("utf-8"))
    return True, True


def restart_docker_container():
    docker_container = os.getenv("DOCKER_CONTAINER")
    os.system(f"docker restart {docker_container}")


if __name__ == "__main__":
    for env in ("OTP_SECRET", "AWS_PROFILE", "DOCKER_CONTAINER"):
        assert os.getenv(env), f"{env} is not set"
    aws_profile = os.getenv("AWS_PROFILE")
    while True:
        command = f"aws sts get-caller-identity --profile {aws_profile}"
        login_success, need_reload = start_command_with_input(command, get_otp_code())
        if login_success:
            if need_reload:
                restart_docker_container()
            print("Success reloading AWS Login")
            print("Waiting for next login try ...")
            time.sleep(30)
        else:
            print("Error running AWS Login")
            break
