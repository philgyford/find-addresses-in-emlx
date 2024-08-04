# Find 'From' addresses in folder of emlx files

This script will traverse a folder containing `.emlx` Apple Mail files, and output information about which email addresses and domains have sent the most emails in it.

I've only tried this on macOS, using mailbox folders created by Mail.app, and running Python 3.12.

## Usage

1.  Check out or download this repository.

2.  Install the [Emlx Parser](https://github.com/terhechte/emlx) module:

	```shell
	pip install -r requirements.txt
	```

3.  Run the script, passing it the path to a folder containing `.emlx` files. e.g.:

	```shell
	./find.py /Users/bob/Library/Mail/V10/900DAD94-6138-4ED8-8C6B-CD8061D5108E/Spam.mbox
	```

    If you're using macOS, Mail.app keeps its mail folders in your `~/Library` directory, at a path similar to that shown above. By default this isn't visible in the Finder but there are [several ways to show it](https://kb.mit.edu/confluence/display/istcontrib/How+to+make+your+Library+folder+visible+in+the+Finder+in+OS+X+10.9+%28Mavericks%29+or+later).

## Example output

It will display two tables based on the "From" lines of all the emails found:

1. A list of email addresses, with the number of times that address sent an email in the mailbox. The third column is a comma-separated list of names used by that email address in the mailbox
2. A list of domains used by those email addresses, and the number of times they appeared.

```
Email addresses:
4  peterbrownservicesinc@gmail.com      Peter Brown
4  mynameissarahsmith@gmail.com         Sarah Smith
3  noreply@cpanel.com                   Restoredesk.example.com
3  katyellis92734@outlook.com           Katy, Katy Ellis, Katy E.
3  andrewkent.technology.ltd@gmail.com  Andrew Kent
3  spolily@chocola.world                SPOTIFY

Domains:
44  gmail.com
12  infinstall.de
10  outlook.com
6   webtechmine.com
6   globalgns.com
4   netflix.com
3   cpanel.com
3   mail.com
3   cenprot-sp.com.br
3   soluxion.co.uk
3   chocola.world
3   wt.ttn.ne.jp
3   servidor
```

## Options

### `-t n`, `--threshold=n`

Only list addresses and domains used more than `n` times. Default is `2`. e.g.:

```shell
./find.py /Users/bob/Library/Mail/V10/900DAD94-6138-4ED8-8C6B-CD8061D5108E/Spam.mbox -t 4
```

or:

```shell
./find.py /Users/bob/Library/Mail/V10/900DAD94-6138-4ED8-8C6B-CD8061D5108E/Spam.mbox --threshold=4
```

### `-v`, `--verbose`

By default the output will be like the example shown above. If this flag is added then it will also list the paths to every `.emlx` file the script parses. e.g.:

```shell
./find.py /Users/bob/Library/Mail/V10/900DAD94-6138-4ED8-8C6B-CD8061D5108E/Spam.mbox -v
```

or:

```shell
./find.py /Users/bob/Library/Mail/V10/900DAD94-6138-4ED8-8C6B-CD8061D5108E/Spam.mbox --verbose
```

## Why?

Every so often I like to check my Spam mailbox and find any 'From' addresses that are used frequenly, and block them entirely. I wrote this script to make it easier to find which addresses to block.

But it might have other uses – it's up to you.


## Credits

By Phil Gyford  
https://www.gyford.com  
phil@gyford.com
