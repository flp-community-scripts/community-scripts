(working draft)

> please comment on these variants in the main repo

# variant 1

A header **must** be present at the top of **every** **\*.pyscript** file. 
> One exception allowed: `#! /.../python3\n`
```python
"""
author: Author 1, Author 2, Author 3
description: Multiline, descriptions
	of the project
category: {category}

"""
```

# variant 2

A header **must** be present at the top of **every** **\*.pyscript** file.
The header format is based on the [Google styleguide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings).

> One exception allowed: `#! /.../python3\n`

```python
"""Short summary about your script.

After a blank line, a long description can follow. Ideally, don't hide usage notes in here, they belong in the form visible to the user. Instead, try to give an overall explanation about the code.
After that, the specs are listed, separated by blank lines. The specs' headers are not indented, but their bodies are.

Author:
	{author 1}
	{author 2}
	{author 3}

Category:
	{category}

Changelog:
	{version, changes}

License:
	{License text}
"""
```