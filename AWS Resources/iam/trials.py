from tokenize import maybe
import boto3 
import json 
import os 


creds_file = "/Users/c1oud4o4/Desktop/iam/cert.json"
f1 = open(creds_file)
request_data = json.load(f1)
#print(request_data['accesss_key'])
#print('')
#print(request_data['secret_key'])

session = boto3.Session(aws_access_key_id=request_data['accesss_key'],aws_secret_access_key=request_data['secret_key'])
#iam = session.resource('iam')
iam_cl = session.client('iam')

username = []
user_id = []
users = iam_cl.list_users()['Users']

for i in users:
    username.append(i['UserName'])
    user_id.append(i['UserId'])
    


#mfa = iam_cl.get_user(UserName='danieleje') #.get_account_summary()
#print(mfa)

pol = iam_cl.list_attached_user_policies(UserName='derrick.vincent') #['AttachedPolicies']

#print(len(pol.key['PolicyName']))
print(pol[['AttachedPolicies']['PolicyName']])


#{'UserName':[], 'policyName':[], 'no_of_policy':[], 'MFA':[]}

#new_list = [{'UserName':a, 'policyName':b, 'no_of_policy':c, 'MFA':d} for a,b,c,d in zip(my_dict['UserName'], my_dict['policyName'], my_dict['no_of_policy'], my_dict['MFA'])]
     
    
#    new_json = json.dumps(new_list)
