# bratreader
Python code for reading Brat Repositories.

# Version

1.1

# License

GPL v3.0

# Installation

Currently, there are no particular installation instructions. Because BratReader will be used so locally, we assume users will be able to figure out themselves where they want to use the code in their project.

# Usage

To use BratReader, simply import repomodel and point it to the directory containing both your `.ann` and `.txt` files.

```python
from bratreader.repomodel import RepoModel

r = RepoModel("path/to/bratfolder") # load repomodel
r.documents            			    # all documents in your brat corpus

doc = r.documents["001"] 			# get document with key 001
print(doc.sentences)    			# a list of sentences in document
print(doc.annotations)  			# the annotation objects in a document

# Save to XML
r.save_xml("my_folder")
# This creates one XML document per original document
# in the specified folder.
```
