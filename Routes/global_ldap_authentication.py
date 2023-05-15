from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException, LDAPBindError
 
def global_ldap_authentication(user_name, user_pwd):
    # fetch the username and password
    print(user_name)
    ldap_user_name = user_name.strip()
    ldap_user_pwd = user_pwd.strip()
 
    # ldap server hostname and port
    ldsp_server = f"LDAP://PE1DCONTROLLER01.coolsupport.rita"
 
    # dn    
    root_dn = "OU=IT,OU=Headquarters Users,OU=Headquarters,DC=coolsupport,DC=rita"
 
    # user
    user = f'cn={ldap_user_name},{root_dn}'
 
    print(user)
    server = Server(ldsp_server, get_info=ALL)
 
    connection = Connection(server,
                            user=user,
                            password=ldap_user_pwd)
    if not connection.bind():
        print(f" *** Cannot bind to ldap server: {connection.last_error} ")
        l_success_msg = f' ** Failed Authentication: {connection.last_error}'
    else:
        print(f" *** Successful bind to ldap server")
        l_success_msg = 'Success'
 
    return l_success_msg