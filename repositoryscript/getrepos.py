import json
import os
import re
from subprocess import call
from github import Github

path = os.path.dirname(os.path.realpath(__file__))

#json loads info
secretinfo = json.load(open(str(path) + '/secretinfo'))

#login
g_user = Github(secretinfo['username'],secretinfo['password']).get_user()

#get repos, sory from newest to oldest of last modified
repos     = sorted(g_user.get_repos(), key=lambda r: r.pushed_at, reverse=True)
repo_size = len(repos) - 1
repo_indx = 1

def display(i,k):
    """
        Displays numbered repos between i and k
        If out of range, does nothing
    """
    if(i > repo_size or i < 0):
        return

    if(k > repo_size or k < 0):
        return

    for item in range(i-1,k):
        print()
        print(str(item+1) + ") " +str(repos[item].name))
        print("----")
        print("Description: " + str(repos[item].description))
        print()

    return 

def display_help():
    """
        Displays help screen
    """
    print("""You have a few options.
                h        - Help
                q        - Quit
                s <str>  - Search for string in repos 
                l <str> - Creates a new repository
                n        - Shows next 5 repositories... (loops back around)
                n # #    - Shows repositories from first number to next
                c # ...  - A sequence of integers E.G. "1 2 3 4" corresponding
                to which repositories you want to clone in the 
                current directory
          """)
    return

def search(string):
    """
        Searches for some string in repos
    """
    found_something = False
    for i in range(len(repos)):
        if(check(repos[i].name,string) or check(repos[i].description,string)):
            display(i+1,i+1)
            found_something = True

    if(not found_something):
        print("Did not find anything")

    return

def check(string,inp):
    """
        Checks to see if string is in inp
    """
    return re.compile(str(inp)).match(str(string))

def create_repo(string):
    """
        Creates a repo with the name of the string and prints the url
            (Adds directory, creates remote, adds readme, adds, commits,push)
    """
    if(not os.path.exists("./" + str(string))):
        print("Creating Directory")
        os.makedirs("./" + str(string)) 
        print("Creating Repo")
        os.chdir("./" + str(string))
        url = g_user.create_repo(string).clone_url
        call("git init; git remote add origin " + str(url),shell=True)
        print("Done")
    else:
        print("Could not create repo")
    return


def step():
    """
        Option flag processing, if a command is not recognized, just re-reuns
    """
    global repo_indx
    global repo_size
    next_step = input("repograbber>")
    if(next_step == "h"):
        display_help()
        return 1

    if(next_step == ""):
        print("Enter h for help")
        return 1

    if(next_step == "q"):
        return -1
    
    split_string = next_step.split(" ")
    if("s" == split_string[0] and len(split_string) > 1):
        search(split_string[1])
        return 1

    if(next_step == "n"):
        if(repo_indx+5 > repo_size):
            incr = (repo_indx+5 - repo_size)
            display(repo_indx,repo_indx+incr)
            repo_indx = 0
        elif(repo_indx == repo_size):
            repo_indx = 0

        display(repo_indx,repo_indx+5) 
        repo_indx += 5
        return 1        

    if("n"  == split_string[0] and len(split_string) > 1):
        if(split_string[1].isdigit() and split_string[2].isdigit()):
            display(int(split_string[1]),int(split_string[2]))
        return 1

    if("c" == split_string[0] and len(split_string) > 1): 
        for i in split_string:
            if i.isdigit() and int(i) <= repo_size:
                url = repos[int(i)-1].clone_url
                os.system('git clone ' + url)

    if("l" == split_string[0] and len(split_string) > 1):
        create_repo(split_string[1])

    return 1

if __name__ == "__main__":
    while(step() != -1):
        continue
