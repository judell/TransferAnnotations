from hypothesis import HypothesisUtils, HypothesisAnnotation

source_usernames = ['USER1', 'USER2']
urls = ['URL1', 'URL2']
target_username = 'TARGET_USERNAME'
target_token = 'TARGET_USERNAME_TOKEN'

h = HypothesisUtils(target_username, target_token)  

def transfer():
    """ given a set of urls and users, copy (public) annotations to another users's account """ 
    for url in urls:
        for source_username in source_usernames:
            params = { 'uri' : url }
            rows = h.search_all(params)
            for row in list(rows):  # capture the original result set, else it'll keep growing as items are posted!
                anno = HypothesisAnnotation(row)
                if anno.user not in source_usernames:
                    continue
                row['user'] = row['user'].replace(source_username, target_username)
                permissions = row['permissions']
                permission_fields = ['admin','update','delete']
                for field in permission_fields:
                    permissions[field][0] = permissions[field][0].replace(source_username, target_username)
                row['permissions'] = permissions
                del row['created']
                del row['updated']
                del row['id']
                h.post_annotation(row)

if __name__ == '__main__':
    transfer()




