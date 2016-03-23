from hypothesis import HypothesisUtils, HypothesisAnnotation
import traceback

source_usernames = ['USER1', 'USER2']
urls = ['URL1', 'URL2']
target_username = 'TARGET_USERNAME'
target_token = 'TARGET_USERNAME_TOKEN'

h = HypothesisUtils(target_username, target_token)

def transfer():
    """ given a set of urls and users, copy (public) annotations to another users's account """ 
    for url in urls:
        for source_username in source_usernames:
            params = { 'uri' : url, 'user': source_username }
            rows = list(h.search_all(params))  # use list() to capture the generator's output or it grows as items are posted!
            if len(rows) > 0:
                print 'url %s user %s rows %d' % (url, source_username, len(rows))
            for row in rows: 
                anno = HypothesisAnnotation(row)
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

def check():
    source_usernames.append(target_username)
    h = HypothesisUtils(target_username, target_token) 
    for url in urls:
        for source_username in source_usernames:
            params = { 'uri' : url, 'user': source_username }
            try:
                rows = list(h.search_all(params))
                if len(rows) > 0:
                    print 'url %s user %s rows %d' % (url, source_username, len(rows))
            except:
                print '%s %s' % ( source_username, url)
                print traceback.print_exc
                continue

if __name__ == '__main__':
    transfer()
    check()
