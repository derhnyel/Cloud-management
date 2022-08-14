import boto3 
import json
import os

class iam:
    def __init__(self):
        self.creds_file= "../certs/AWS/cert.json"
        f1 = open(self.creds_file)
        request_data = json.load(f1)
        session = boto3.Session(aws_access_key_id=request_data['Accesss_Key'],aws_secret_access_key=request_data['Secret_Key'])
        self.iam_cl = session.client('iam')

    def list_users(self):
        users = self.iam_cl.list_users()
        try:
            #my_dict = {'UserName':[], 'UserId':[]}
            UserId = []
            for i in users['Users']:
                UserId.append(i['UserName'])
                #my_dict['UserName'].append(i['UserName'])
                #my_dict['UserId'].append(i['UserId'])
            while 'Marker' in users:
                response = self.iam_cl.list_users(Marker=users['Marker'])
                for user in response['Users']:
                    UserId.append(user['UserName'])
            #new_list = [{'UserName':i, 'UserId':g} for i,g in zip(my_dict['UserName'], my_dict['UserId'])]
            return UserId
        except Exception as e:
            return e
    
    def get_mfa(self):
        mfa_users = []
        try:
            iam_userss = self.list_users()
            for iam_user in iam_userss:
                response = self.iam_cl.list_mfa_devices(UserName=iam_user)
                if not response['MFADevices']:
                    mfa_users.append({'UserName': iam_user, 'MFA': "NOT Enabled"}) #iam_user)
                else:
                    mfa_users.append({'UserName': iam_user, 'MFA': "Enabled"}) #iam_user)
            return mfa_users
        except Exception as e:
            return e

    def get_permission_boundry(self):
        my_dict = {'UserName':[], 'policyName':[], 'no_of_policy':[], 'MFA':[]}
        try:
            ids = self.list_users()
            for i in ids:
                response = self.iam_cl.list_mfa_devices(UserName=i)
                policies = self.iam_cl.list_attached_user_policies(UserName=i)['AttachedPolicies']
                my_dict['UserName'].append(i)
                my_dict['no_of_policy'].append(len(policies))
                if not response['MFADevices']:
                    my_dict['MFA'].append('NOT Enabled')
                else:
                    my_dict['MFA'].append('Enabled')
                new_list = []
                for poliicy in policies:
                    new_list.append(poliicy['PolicyName'])
                my_dict['policyName'].append(new_list)

            new_list = [{'UserName':a, 'policyName':b, 'no_of_policy':c, 'MFA':d} for a,b,c,d in zip(my_dict['UserName'], 
            my_dict['policyName'], my_dict['no_of_policy'], my_dict['MFA'])]

            new_json = json.dumps(new_list)
            #with open('/Users/c1oud4o4/Desktop/iam/trial.json', 'a') as file:
                #file.write(new_json)
                #file.close()
            return new_json 
        except Exception as e:
            return e
    
    def create_user(self, New_UserName=str(), Password=str(), PolicyName=str()):
        try:
            created_user = self.iam_cl.create_user(UserName=New_UserName)
            if created_user['User']['UserName']:
                arn_split = created_user['User']['Arn'].split(':')
                attach_policy = self.iam_cl.attach_user_policy(UserName = New_UserName, PolicyArn = f'arn:aws:iam::aws:policy/{PolicyName}')
                login_profile = self.iam_cl.create_login_profile(UserName=New_UserName, Password=Password)
                username = str(created_user['User']['UserName'])
                #open('login.json', 'a').write({'Status': 'User Created', 'Priviledge': f'{PolicyName}', 'Account_ID':f'{str(arn_split[4])}', 'UserName': f'{username}', 'PassWord': f'{str(Password)}'})
                return {'Status': 'User Created', 'Priviledge': f'{PolicyName}', 'Account_ID':f'{str(arn_split[4])}', 'UserName': f'{username}', 'PassWord': f'{str(Password)}'}
            else:
                return 'Failed to create a New User'
        except Exception as e:
            return e

    def delete_user_policy(self, Username=str(), PolicyName=str()):
        try:
            delete = self.iam_cl.delete_user_policy(UserName=Username,PolicyName=PolicyName)
            return f'{PolicyName} deleted from IAM user -> {Username}'
        except Exception as e:
            return e

    def delete_user(self, UserName=str())->str:
        try:
            delete = self.iam_cl.delete_user(UserName=UserName)
            return f'{UserName} has been deleted from Iam users'
        except Exception as e:
            return e














    
'''

iam_users = iam("/Users/c1oud4o4/Desktop/iam/cert.json").list_users()
#print('users without mfa')
#print(iam("/Users/c1oud4o4/Desktop/iam/cert.json").get_mfa(iam_users)) 
print('username policieslevel count')
print(iam("/Users/c1oud4o4/Desktop/iam/cert.json").get_permission_boundry(iam_users)) 
'''
