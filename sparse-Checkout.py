#!/usr/bin/env python3
 
 
import os 
from  os.path import split as split_path
from argparse import ArgumentParser

class Repo:
    def __init__(self,url):
        if(not url.startswith('https://github.com')):
            return 

        if(url.endswith('.git')):
            url = url[:-4]

      
        attribs=[]
        attrib =''    
        while  attrib != 'github.com':
            url, attrib = split_path(url)
            attribs.append(attrib)

        attribs.pop() #poop  'github.com'

        count = len(attribs)
        if (count >= 5 ):
            self.branch ,self.type ,self.name,self.owner= attribs[count - 4:count  ]
            for i in reversed(attribs[:count-4]):
                self.path += f"/{i}"
        elif count == 2: 
            self.name,self.owner= attribs 
        else:
            raise RuntimeError('invalid url')  

    def is_valid(self):
        if ((self.name =='' )or (self.owner =='')):
            return False
        return True

    def is_checkoutable(self):
        if( not  self.is_valid() or
            self.type != 'tree' or 
            self.branch=='' or 
            self.path=='') :
            return False
        return True
             

    def as_url(self):
        if(self.is_valid()):
            return f"https://github.com/{self.owner}/{self.name}.git"

    def as_url_path(self):
        if self.is_checkoutable():
            return f"https://github.com/{self.owner}/{self.name}/{self.type}/{self.branch}{self.path}.git"

    def print(self):
        print(self.as_url())

    owner =''
    name =''
    type =''
    branch =''
    path =''
         
if  __name__ == "__main__": 
    parser = ArgumentParser()
    parser.add_argument("-u", dest="url",  
                        help="full url address to a github repository's subdirectory")
    parser.add_argument("-add", dest="add",  
                        help="")
    
    args = parser.parse_args()
    
    
    

    repo = Repo(  url=args.url)
    #repo.print()
    #print('is_checkoutable: ',repo.is_checkoutable())

    if(not repo.is_checkoutable()   ):
        raise  RuntimeError(f"can not pull from {args.url}")  

    os.system(f"git clone  {repo.as_url()}  --no-checkout  --depth 1") 
    current_dir = os.getcwd()
    os.chdir(f"{current_dir}/{repo.name}")
    os.system(f"git sparse-checkout  init") 

    f = open(".git/info/sparse-checkout", "a")
    f.write(repo.path)
    f.close()

    os.system(f"git checkout origin/{repo.branch}") 

 