# whisk
# Gabriel Ruoff geruoff@syr.edu, 2021
# A utility which merges static html with php scripts to
# create data-driven sites from website builder freeware

import sys
import os
import re

# append module path
sys.path.append(os.getcwd())

# regexs
startindicator = re.compile(r'#\{php[1-99]}')
endindicator = re.compile(r'#\{/php[1-99]}')
exclude = re.compile(r'#exclude')
endexclude = re.compile(r'#/exclude')

class whisk:
    def __init__(self, htmldir=None, templatedir=None, backupdir=None):
        self.htmldir = htmldir
        self.templatedir = templatedir
        self.backupdir = backupdir

    def build(self, backup=False):
        pagestobuild = []

        print('Whisk -\n')
        print('1. Searching for pages to build in '+self.htmldir)
        # iterate through static html directory
        for filename in os.listdir(self.htmldir):
            # iterate through html files
            if filename.endswith(".html"):
                print(filename)
                # see if there is a php template for this file
                for template in os.listdir(self.templatedir):
                    if template.endswith(".phptemplate") and self.stripextension(template) == self.stripextension(filename):
                        print('\tfound template: ', template)
                        pagestobuild.append(filename)
            else:
                continue

        # back up old php files
        if (backup):
            if self.backupdir is None:
                print(self.warn('backup selected but no backup directory set'))
                print(self.warn('set backup directory with setbackupdir(path)'))
                print('backup set to false, skipping')
                self.abort('nobackupdir')
            else:
                print('\n2. Backing up old php files to '+self.backupdir)
                for filename in pagestobuild:
                    filename = self.stripextension(filename) + '.php'
                    # iterate through target files
                    if filename in os.listdir(self.htmldir):
                        remove = any([s for s in os.listdir(self.htmldir + 'backup') if filename in s])
                        if remove:
                            os.remove(self.htmldir + 'backup\\' + filename)
                        os.rename(self.htmldir + filename, self.htmldir + 'backup\\' + filename)
                print('\t- done')

        # list of pages that will be built from templates
        print('\n3. Building pages from '+self.templatedir)
        for page in pagestobuild[::]:
            print('\t- ' + page)
            self.buildheader(page)
            self.buildpage(page)
            self.buildfooter(page)

        print('\n4. done');

    def sethtmldir(self, path):
        self.htmldir = path.replace('\\', '\\\\')

    def settemplatedir(self, path):
        self.templatedir = path.replace('\\', '\\\\')

    def setbackupdir(self, path):
        self.backupdir = path.replace('\\', '\\\\')

    def stripextension(self, filename):
        return os.path.splitext(filename)[0]


    def removeexcluded(self, filename):
        with open(self.templatedir+self.stripextension(filename)+'.phptemplate') as f:
            buffer = [[]]
            templatecontent = f.readlines()
            for i, line in enumerate(templatecontent):
                if exclude.match(line):
                    for j, line2 in enumerate(templatecontent):
                        if endexclude.match(line2):
                            buffer[0].append([i, j])
        for i in range(int(len(buffer[0]))):
            # -1 to exclude exclude tag
            for j in range(buffer[0][i][1], buffer[0][i][0]-1, -1):
                templatecontent.pop(j)
        return templatecontent


    def selectcodefromtemplate(self, filename, indicatorstr):

        templatecontent = self.removeexcluded(filename)

        for i, line in enumerate(templatecontent):
            # if line matches exclude
            # print(indicatorstr[:2]+'/'+indicatorstr[2:])
            if indicatorstr in line:
                for j, line2 in enumerate(templatecontent):
                    if indicatorstr[:2]+'/'+indicatorstr[2:] in line2:
                        templatecontent[i] = templatecontent[i].replace(indicatorstr,"<!-- " + indicatorstr[0] + '!' + indicatorstr[1:] + " -->")
                        return templatecontent[i:j]

    def buildheader(self, filename):
        # load page content into an array
        with open(self.htmldir + self.stripextension(filename) + '.html', 'r') as f:
            pagecontent = f.readlines()
            # pagecontent = [x.strip() for x in f.readlines()]
            f.close()

        buffer = self.selectcodefromtemplate(filename, "#{head}")
        if buffer:
            print('\t  - building header')
            buffer.extend(pagecontent)

            with open(self.htmldir + self.stripextension(filename) + '.php', 'w') as f:
                f.write("".join(buffer))
                f.close()


    def buildfooter(self, filename):
        # load page content into an array
        with open(self.htmldir + self.stripextension(filename) + '.php', 'r') as f:
            pagecontent = f.readlines()
            # pagecontent = [x.strip() for x in f.readlines()]
            f.close()

        buffer = self.selectcodefromtemplate(filename, "#{foot}")
        if buffer:
            print('\t  - building footer')
            pagecontent.extend(buffer)

            with open(self.htmldir + self.stripextension(filename) + '.php', 'w') as f:
                f.write("".join(pagecontent))
                f.close()


    def buildpage(self, filename):
        print('\t  - building page')
        # load page content into an array
        with open(self.htmldir+self.stripextension(filename)+'.php', 'r') as f:
            pagecontent = f.readlines()
            # pagecontent = [x.strip() for x in f.readlines()]
            f.close()

        original_length = len("".join(pagecontent).split('\n'))

        # iterate throught the page contents
        results = []
        for i, line in enumerate(pagecontent):
            # print(line)
            # look for a template indicator
            _results = startindicator.findall(line)
            if _results:
                results.append([_results[0], i])
                # print('found ' + result.group(0))

        # look for this indicator in the html file and move php code into buffer
        # print(results)
        for result in results:
            for i, line in enumerate(pagecontent):
                if result[0] in line:
                    break
            buffer = self.selectcodefromtemplate(filename, result[0])

            # insert code into static page
            splitline = pagecontent[i]
            indicatorstr = startindicator.search(splitline).group(0)
            linestart = splitline.index(indicatorstr)
            lineend = linestart + len(indicatorstr)
            # print(linestart, lineend)
            pagecontent = pagecontent[:i] + [pagecontent[i][:linestart]] + buffer + [pagecontent[i][lineend:]] + pagecontent[i+1:]
            with open(self.htmldir + self.stripextension(filename) + '.php', 'w') as f:
                f.write("".join(pagecontent))
                f.close()

            #refresh
            with open(self.htmldir + self.stripextension(filename) + '.php', 'r') as f:
                pagecontent = f.readlines()
                f.close()

    def warn(self, warning):
        print('!- warning: '+str(warning))

    def abort(self, err):
        sys.exit(err)
