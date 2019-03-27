#ex

DEPLOY_LANG = {
    'php' : {'name':'php',
            'repo_name' : 'php-getting-started',
            'link': 'https://github.com/heroku/php-getting-started.git',
            'command' : 'git clone https://github.com/heroku/php-getting-started.git'},

    'python' : {'name':'python',
            'repo_name' : 'python-getting-started',
            'link': 'https://github.com/heroku/python-getting-started.git',
            'command' : 'git clone https://github.com/heroku/python-getting-started.git'},

    'go' : {'name':'go',
            'repo_name' : 'go-getting-started',
            'link': 'https://github.com/heroku/go-getting-started.git',
            'command' : 'git clone https://github.com/heroku/go-getting-started.git'},
}

#print DEPLOY_LANG['go']['clone_command']
#print DEPLOY_LANG['php']['link']
