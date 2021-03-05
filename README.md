# whisk

### Whisk is a utility to combine PHP scripting with generated static html in order to easily build data-driven sites. 
There are many tools available which allow users to produce visually appealing static HTML pages from a simple drag-and-drop interface. While convient and powerful, popular software in this space such as [Wordpress](https://wordpress.com), [Squarespace](https://squarespace.com), [Jekyll](https://jekyllrb.com/), or [Hugo](https://gohugo.io/) lack the functionality for users to integrate php scripting into their webpages.

Web scripting languages such as php allow developers to create dynamic, database-driven sites and web-based applications, however testing php scripts and integrating them into html pages is very inefficient. When html is exported from a generator, corresponding sections of php code must be copy-pasted direcly into each html document, then each document much be renamed to a .php file. When developers are updating static html with high frequency or working with large numbers of pages, this process becomes very inefficient.

Whisk takes [two files of the same name](https://github.com/gabrielruoff/whisk/edit/main/README.md#File Types:): 'static', an .html file containing static html code and 'template', a .phptemplate file containing specially formatted php code and outputs a single, similarly named .php file. It does this by locating unique 'tags' in the static file before inserting the tag's corresponding section of php code, defined in the template, into the file inplace of the tag.

These sections can be denoted in the static file via directly modifying the source html, or natively in popular web builder applications by placing a designating 'custom html' block that contains the desired tag.

There are four types of tags: code section, head, foot, and exclude. Code sections contain code to be inserted into the input static in a designated location. Head sections contain code to be inserted at the very top of the output file (which is required for using sessions, etc..) while Foot sections contain code to be inserted at the very bottom of the input .html file. A list of tags and their usages can be found [below](https://github.com/gabrielruoff/whisk/edit/main/README.md#Tags:).

As shown in the [example code](https://github.com/gabrielruoff/whisk/edit/main/README.md#Example Code:) section, whisk takes two directories as input - a directory containing static html files and a directory containing corresponding .phptemplate files. When run, it outputs .php files for each valid static-html-template input pair that it has found. Additionally, the user can define a backup directory to which all .php files existing in the static html source directory at runtime will be moved to. This ensures existing files are not accidentally written over if the user did not intend to run whisk.

## Tags:
### This utility inserts php code into static html at the specified tag
1. Code section - indicates a section of code to insert
- open code section: '#\{php<tag number>}' | example: '#\{php1}' | regex: '#\{php[1-99]}'
- close code section: '#\{/php<tag number>}' | example: '#\{/php1}' | regex: '#\{/php[1-99]}'

2. Head section (may be used once per file) - indicates a section of code to insert into static html at the top of the file
- open head section: '#\{head}' | example: '#\{head}' | regex: '#\{head}'
- close head section: '#\{head}' | example: '#\{/head}' | regex: '#\{/head}'

3. Foot section (may be used once per file) - indicates a section of code to insert into static html at the bottom of the file
- open foot section: '#\{foot}' | example: '#\{foot}' | regex: '#\{foot}'
- close foot section: '#\{foot}' | example: '#\{/foot}' | regex: '#\{/foot}'

3. Exclude section - indicates a section of code to exclude when into static html
- open exclude section: '#exclude' | example: '#exclude' | regex: '#exclude'
- close exclude section: '#/exclude' | example: '#/exclude' | regex: '#/exclude'
 
 
## File types:

### Static files:
 - extension: .html
 - place a tag inside your static html where you want a corresponding section of php to be inserted.
 - ex:
 `<static html>
 <static html>
 <static html>
 #{php1}
 <static html>
 <static html>
 <static html>`
 
 ### PHP template files:
 - extension: .phptemplate
 - place a open and close tag around a corresponding seciton of code
 - ex:
 `<unwanted code>
 #{php1}
 <wanted code>
 <wanted code>
 #exclude
 <excluded code>
 <excluded code>
 #{/php1}
 <unwanted code>`
  
 In the above example, the produced php file would be
 - note: whisk will convert the php tag in your input file to an html comment containing a slightly modified tag, as seen below
 `<static html>
 <static html>
 <static html>
 <!-- #!{php1} -->
 <wanted code>
 <wanted code>
 <static html>
 <static html>
 <static html>`


## Example Code:
import the whisk module
`from whisk import whisk`

initialize a whisk instance - the html source, template, and backup directories may either be specified in the constructor or after initialization*
`w = whisk(htmldir = X:\\docker\\data\\www\\html\\', templatedir = 'X:\\docker\\data\\phplib\\sitebuilder templates\\')`

\*if these directories were not specified at initialization, set them
`w.sethtmldir('X:\\docker\\data\\www\\html\\')`
`w.settemplatedir('X:\\docker\\data\\phplib\\sitebuilder templates\\')`

set a backup directory
`w.setbackupdir('backup')`

build php files with backup enabled
`w.build(backup=True)`

backup can be skipped with simply
`w.build()`
