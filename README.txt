Hello!

This is a Twitch bot which charges StreamLabs currency to press buttons or move the mouse on your computer.


This is just a side project of mine, I couldn't find many bot codes that integrate with StreamLabs, so I figured I would post it.
It's written in Python 2.7, and there is plenty of room to improve or modify it to your needs.

I've put #TODO: 's in anywhere user-specific information is needed.

YOU WILL NEED TO REGISTER A BOT WITH STREAMLABS, AND REQUEST CURRENCY ACCESS FOR THIS BOT TO WORK.
Access to modify currency isn't given by default, so you will have to request it from them. The process is very simple, and Aaron is super helpful.

I will not be providing support or updates for this; it was more an experiment on my end.

Cheers!
-Grant 'Galad' Roberts

--Edits: 
-The bot will take a second to connect to Twitch, you can check if it has connected with the "!testing" command.
-When the script asks for a code, it is referring to the code at the end of the redirect URL, after you have allowed it access through StreamLabs.
		
		It will look something like: http://localhost:8888/callback?code=***THIS IS THE PART IT IS ASKING FOR***
		
		The page itself will simply say "This Site Can't Be Reached"
