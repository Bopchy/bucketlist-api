errors = {
    'UserAlreadyExistsError': {'message': 'A user with that username already exists', 'status': 409},
    'UsernameRequiredError': {'message': 'No username provided', 'status': 400},
    'EmailRequiredError': {'message': 'No email provided', 'status': 400},
    'PasswordRequiredError': {'message': 'No password provided', 'status': 400},
    'InappropriateEmailError': {'message': 'Wrong email format provided.', 'status': 422},
    'EmailAlreadyExistsError': {'message': 'A user with that email already exists', 'status': 409},
    'NonExistingUserError': {'message': "A user with that username doesn't exist.", 'status': 401},
    'WrongPasswordUsedError': {'message': 'Incorrect password.', 'status': 401}
}