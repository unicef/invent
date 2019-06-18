import argparse
import subprocess
import traceback

from passlib.utils import ab64_encode, ab64_decode

UID_PATH = './uidnumber'
USER_ACCOUNT_FILENAME = "user_account.ldif"
CHANGE_PASS_FILENAME = "change_password.ldif"
ACCOUNT_LDIF_PATH = './' + USER_ACCOUNT_FILENAME
CHANGE_LDIF_PATH = './' + CHANGE_PASS_FILENAME
LDAP_ADMIN_PASS = "admin"
LDAP_SYNC_PATH = '/container/service/slapd/assets'

parser = argparse.ArgumentParser()
parser.add_argument("username", help="username")
parser.add_argument("hash", help="password hash value")
parser.add_argument("--update", action='store_true', help="user update only")
args = parser.parse_args()


def convert_django_SHA256_to_ldap(django_hash):
    hash = django_hash.split('$')
    django_alg, django_rounds, django_salt, django_dk = hash

    ldap_alg = '{PBKDF2-SHA256}'
    ldap_rounds = '30000'
    ldap_salt = ab64_encode(django_salt.encode()).decode('ascii')
    ldap_dk = ab64_encode(ab64_decode(django_dk)).decode('ascii')

    assert ldap_rounds == django_rounds

    return ldap_alg + '{}${}${}'.format(ldap_rounds, ldap_salt, ldap_dk)


def make_user_account_ldif(username, password_hash):
    try:
        with open(UID_PATH, "r+") as u:
            uid_number = int(u.read())

            with open(ACCOUNT_LDIF_PATH, "w") as f:
                f.truncate()

                ldap_hash = convert_django_SHA256_to_ldap(password_hash)
                uid_number += 1

                ldap_account_ldif = [
                    "dn: uid={},ou=people,dc=example,dc=org".format(username),
                    "cn: {}".format(username),
                    "givenName: {}".format(username),
                    "sn: {}".format(username),
                    "uid: {}".format(username),
                    "uidNumber: {}".format(uid_number),
                    "gidNumber: 503",
                    "homeDirectory: /home/users/{}".format(username),
                    "loginShell: /bin/bash",
                    "objectClass: top",
                    "objectClass: inetOrgPerson",
                    "objectClass: posixAccount",
                    "userPassword: {}".format(ldap_hash),
                    "",
                    "dn: gidNumber=503,ou=default_prefix,ou=groups,dc=example,dc=org",
                    "changetype: modify",
                    "add: memberUid",
                    "memberUid: {}".format(username),
                ]
                lines = '\n'.join(ldap_account_ldif)
                f.writelines(lines)

            u.seek(0)
            u.truncate()
            u.write(str(uid_number))

        return True, "User created: {}".format(username)
    except:
        return False, traceback.format_exc()


def change_user_password_ldif(username, password_hash):
    try:
        with open(CHANGE_LDIF_PATH, "w") as f:
            f.truncate()

            ldap_hash = convert_django_SHA256_to_ldap(password_hash)

            ldap_pass_ldif = [
                "dn: uid={},ou=people,dc=example,dc=org".format(username),
                "changetype: modify",
                "replace: userPassword",
                "userPassword: {}".format(ldap_hash),
            ]
            lines = '\n'.join(ldap_pass_ldif)
            f.writelines(lines)

        return True, "Password changed: {}".format(username)
    except:
        return False, traceback.format_exc()


def get_ldap_sync_container_id():
    docker_ps_cmd = subprocess.Popen(["docker", "ps", "-f",
                                      'label=com.docker.swarm.service.name=syncldap_ldap-service', "--format",
                                      "'{{.ID}}'"], stdout=subprocess.PIPE)
    docker_ps_cmd.wait()
    ldap_sync_container_id = docker_ps_cmd.stdout.read().decode('utf-8').strip().replace("'", "")
    return ldap_sync_container_id


def copy_ldif_to_container(ldap_sync_container_id, filename):
    docker_cp_cmd = subprocess.Popen(
        ["docker", "cp", filename, "{}:{}".format(ldap_sync_container_id, LDAP_SYNC_PATH)])
    docker_cp_cmd.wait()


def import_user_ldif_to_ldap(ldap_sync_container_id):
    docker_exec_cmd = subprocess.Popen(["docker", "exec", ldap_sync_container_id,
                                        "ldapadd", "-cxD", "cn=admin,dc=example,dc=org",
                                        "-w", LDAP_ADMIN_PASS,
                                        "-f", "{}/{}".format(LDAP_SYNC_PATH, USER_ACCOUNT_FILENAME)])
    docker_exec_cmd.wait()


def import_change_ldif_to_ldap(ldap_sync_container_id):
    docker_exec_cmd = subprocess.Popen(["docker", "exec", ldap_sync_container_id,
                                        "ldapmodify", "-H", "ldap://", "-x", "-D", "cn=admin,dc=example,dc=org",
                                        "-w", LDAP_ADMIN_PASS,
                                        "-f", "{}/{}".format(LDAP_SYNC_PATH, CHANGE_PASS_FILENAME)])
    docker_exec_cmd.wait()


if __name__ == '__main__':
    if args.update:
        success, msg = change_user_password_ldif(username=args.username, password_hash=args.hash)
    else:
        success, msg = make_user_account_ldif(username=args.username, password_hash=args.hash)

    if success:
        ldap_sync_container_id = get_ldap_sync_container_id()
        if args.update:
            copy_ldif_to_container(ldap_sync_container_id, CHANGE_PASS_FILENAME)
            import_change_ldif_to_ldap(ldap_sync_container_id)
        else:
            copy_ldif_to_container(ldap_sync_container_id, USER_ACCOUNT_FILENAME)
            import_user_ldif_to_ldap(ldap_sync_container_id)

    print(msg)
