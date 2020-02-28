# How to publish with Pelican

* Run Pelican to generate the static HTML files in **output**:

    ```zsh
    $ pelican content -o output -s publishconf.py
    ```

* To view the site you start the built in pelican server:

    ```zsh
    $ pelican --listen
    ```

    Or use the one that comes with Python:

    ```zsh
    $ cd output
    $ python -m http.server
    ```
    
    You can preview the site by bringing up `http://localhost:8000` in your browser.

* Use **ghp-import** to add the contents of the **output** directory to the **master** branch:

    ```zsh
    $ ghp-import -m "Generate Pelican site" --no-jekyll -b master output
    ```

* Push the local master branch to the remote repo:

    ```zsh
    $ git push origin master
    ```

* Commit and push the new content to the **content** branch:

    ```zsh
    $ git add content
    $ git commit -m 'added a first post, a photo and an about page'
    $ git push origin content
    ```
