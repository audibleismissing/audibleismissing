import os.path

import audible


# create audible device
# If you have activated 2-factor-authentication for your Amazon account, you can append the current OTP to your password. This eliminates the need for a new OTP prompt.
def createDeviceAuth(username, password, country_code, auth_file='audible_auth'):
    # Authorize and register in one step
    auth = audible.Authenticator.from_login(
        username,
        password,
        locale=country_code,
        with_username=False
    )

    # Save credentials to file
    auth.to_file(auth_file)


def loadExistingAuth(auth_file='audible_auth') -> audible.Client:
    if doesAuthExist(auth_file):
        return audible.Authenticator.from_file(auth_file)
    else:
        print("Run with parameters to create auth.")
    return None


def doesAuthExist(auth_file='audible_auth') -> bool:
    if os.path.isfile(auth_file):
        return True
    return False


# def removeDevice()
#     auth.deregister_device()
