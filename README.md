Kniteditor Website
==================

You can view this website under [fossasia.github.io/kniteditor][website].
Contributions are welcome. To easy contributing, this site has a detailed [contributing section][contribute].

Contribute
----------

To contribute to this website you can

- [translate][translate] the website into other languages
  - [update translations][update-translations] for existing languages
- [install][install] the website and [change its code][solve-issues].

### Context

We have two branches:

- `gh-pages` serves the static content of the site. Do not edit this. It is generated and your changes will get lost.
- `gh-pages-source` generates the website and should be edited.

### Install

1. Clone the website. This can be done with

        git clone https://github.com/fossasia/kniteditor.git/

2. Checkout the `gh-pages-source` branch.
3. Update the sbmodule in the `_site` directory. [Jekyll][jekyll] generates the site into that directory. Therefore, it should contain the `gh-pages` branch. It can be done like this:

        cd kniteditor
        git submodule init
        git submodule update
        cd _site
        git checkout gh-pages
        ls
        cd ..
        
    Outcome: When doing `ls`, you should see the index.html file and other files that are part of the website as well as folders for different languages.

4. [Install Jekyll][jekyll-tips]. Here for Ubuntu:
  
        sudo apt-get update
        sudo apt-get -y install ruby-full
        sudo apt-get gem install jekyll

5. Install bundler to manage the dependencies:

        sudo gem install bundler
        
6. Install the dependencies:

        bundle install
        
7. Start the website:

        jekyll serve --trace
        
    Now, you can browse [localhost:4000/kniteditor/](http://localhost:4000/kniteditor/) and view the website.

### Solve Issues

You can view all issues of the webste with the [website tag][issues].

### Translate Into Other Languages

You can translate the website into your own langauge.

1. Install [POEdit][poedit]
2. In the [_i18n](_i18n) folder, you can find the translations. Your language has a [language code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).
    Create a folder inside [_i18n](_i18n) with the language code for your language.
3. Open POEdit and "Create new translation".
    Choose the [_i18n/website.pot](_i18n/website.pot).
    Save the file as `website.po` in the folder of your language code.
4. Translate with POEdit.
5. Create a commit and  a [pull-request][pull-request] with the updated files.


### Update Existing Translaions

Existing translations may be outdated.
You can update them with the following process:

1. Install [POEdit][poedit]
2. In the [_i18n](_i18n) folder, you can find the translations. Open the `.po` file of your liking and translate it further.
3. Create a commit and  a [pull-request][pull-request] with the updated files.
 
[website]: https://fossasia.github.io/kniteditor
[jekyll]: http://jekyllrb.com/
[jekyll-tips]: http://jekyll.tips/
[issues]: https://github.com/fossasia/kniteditor/issues?q=is%3Aissue+is%3Aopen+label%3Awebsite
[translate]: #translate-into-otehr-languages
[update-translations]: #update-existing-translations
[solve-issues]: #solve-issues
[poedit]: http://poedit.net/
[pull-request]: https://help.github.com/articles/creating-a-pull-request/
[contribute]: #contribute
