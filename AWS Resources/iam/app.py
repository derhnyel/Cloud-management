from iam_calls import iam

A1 = iam()

#get_users = A1.list_users()

#permission_boundries = A1.get_permission_boundry()
#get_mfa = A1.get_mfa()
#dele_pol = A1.delete_user_policy()
del_user = A1.delete_user('TestUser')

#user = A1.create_user('TestUser', '@yourpassword5287', 'IAMUserChangePassword')



#print(user)
print('permission boundries')
#print(permission_boundries)
print('')
print('')
print('MFA Users')
#print(get_mfa)
print(del_user)
