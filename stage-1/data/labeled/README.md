The entity type that we have marked up in the documents is **Cryptocurrency**.

The markups can be found as follows: 

Everyline in a document is followed by a markup line; the markup line consists of the same number of words as the original line. If the first character of a word in the markup line is a 1, then it means that the corresponding word in the original line is a cryptocurrency that we marked up. Else, it starts with a \`. The rest of the characters of the word are marked with an underline (could have been a 1, but we chose to make an underline for better viewing). If an entity name is two or more words, we simply extend the underscore through the next words, without adding a second mark for the second word of the entity name.

**For example:**

New York: Bitcoin hit a three-week high on Tuesday

\`__ \`____ 1______ \`__ \` \`_________ \`___ \`_ \`______

New York: Bitcoin Cash hit a three-week high on Tuesday

\`__ \`____ 1___________ \`__ \` \`_________ \`___ \`_ \`______

Note: When viewed in some text editors, the characters of the markup lines and original lines line up, making it easier to both mark and see:

![example](https://github.com/dliangsta/cs839-project/blob/master/data/labeled/bitcoin_example.PNG)

The first line is the original line and the second is the markup line. The third word in the original line is a cryptocurrency. Therefore, the third word in the markup line starts with a 1.
