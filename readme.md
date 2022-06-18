# File Manager

This application is based on the TK library. The application supports standard file operations such as:

1. Create a folder
2. Create file
3. Copy folder/file
4. Move folder/file
5. Rename folder/file
6. Delete folder/file

A search function has also been implemented. You can only search among files, but this is temporary, in the future I
will add folder search.
To find the desired file, you need to do the following:

* Change to the directory where you want to find the file.
* In the address input field, add a slash "/", then the name of the file you need to find. Note that the file name must
  be entered along with the file extension.For example:

#### C:\Users\User\Desktop/text.txt

If you don't know the name of a file, but you do know the extension of that file, you can use the "*" sign.
For example:

#### C:\Users\User\Desktop/*.txt

If you do not know the file extension, but you know the full or partial name of this file, you can do a search like
this:

#### C:\Users\User\Desktop/text.*

or this:

#### C:\Users\User\Desktop/text*.txt