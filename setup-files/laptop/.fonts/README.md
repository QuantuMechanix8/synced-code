I have used a total bodge [from here](https://gist.github.com/gbishop/9803b7ecc50b1930407ef4b98d1ba7c9#file-nerd-js) which uses a custom python server to provide the font file, since for some reason crostini doesn't support local font files but does support ones from a url?

I am using the `IosevkaTermNerdFont-Regular.ttf` font file (but you can add any you like to the folder and change `nerd.js` to match)
As written in the github link, goto `chrome://inspect#other`, inspect the terminal.html and run the `nerd.js` code in the console

In settings the font will say JetBrainsMono Nerd Font (trying to change the font family in nerd.js seemed to break things?) - but renders the desired font nonetheless

It seems to work for now but I recognise this is really hacky and likely to break soon
